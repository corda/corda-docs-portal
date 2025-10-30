import re
import os
import sys
import argparse
from difflib import SequenceMatcher

# ----------------------------
# ANSI colors for clarity
# ----------------------------
class Colors:
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ----------------------------
# Normalization and Parsing
# ----------------------------

def normalize_heading(heading: str) -> str:
    """
    Normalize a Markdown heading to its corresponding anchor form.
    """
    heading_text = heading.lstrip('#').strip()
    heading_text = re.sub(r'\s*\{\{<[^>]+>\}\}\s*$', '', heading_text)
    heading_text = heading_text.lower()

    # --- NEW PATCH: handle ` and @ for anchors like "@DoNotImplement" ---
    heading_text = heading_text.replace('`', '')  # remove backticks
    heading_text = heading_text.replace('@', '')  # remove @ symbols
    # -------------------------------------------------------------------

    heading_text = re.sub(r"[():'’,;.`?/*]", "", heading_text)
    heading_text = heading_text.replace(' ', '-')
    return heading_text


def find_headings(markdown: str):
    """Return a dict of normalized→original heading text, handling duplicates with -1, -2, etc."""
    headings = {}
    counts = {}
    for match in re.finditer(r'^(#+)\s+(.*)', markdown, re.MULTILINE):
        original = match.group(2).strip()
        normalized = normalize_heading(match.group(0))
        count = counts.get(normalized, 0)
        counts[normalized] = count + 1
        if count > 0:
            normalized = f"{normalized}-{count}"
        headings[normalized] = original
    return headings


def find_anchors_with_lines(markdown: str):
    """
    Return list of (ref_path, anchor, line_number, line_snippet).
    Supports:
      {{< relref "#anchor" >}}
      {{< relref "../path/file.md#anchor" >}}

    Ignores:
      {{< cenmlatestrelref ... >}}
      {{< cordalatestrelref ... >}}
    """
    anchors = []
    # Find all relrefs excluding the cenmlatestrelref and cordalatestrelref variants
    pattern = re.compile(
        r'{{<\s*(?!cenmlatestrelref|cordalatestrelref)\s*relref\s*["{<]*([^\s"\'>}]+)["}>]*'
    )

    for i, line in enumerate(markdown.splitlines(), start=1):
        # Skip ignored shortcodes explicitly (for safety)
        if "cenmlatestrelref" in line or "cordalatestrelref" in line:
            continue

        for match in pattern.finditer(line):
            raw_ref = match.group(1)
            ref_path, anchor = None, None
            if '#' in raw_ref:
                ref_path, anchor = raw_ref.split('#', 1)
            else:
                ref_path = raw_ref
            if not ref_path or ref_path in ('', '#'):
                ref_path = None
            snippet = line.strip()
            if len(snippet) > 60:
                snippet = snippet[:57] + "..."
            anchors.append((ref_path, anchor, i, snippet))
    return anchors


# ----------------------------
# Caching and Utilities
# ----------------------------

def cache_headings_and_files(folder: str):
    """Build dictionaries for file headings and all known .md files."""
    headings_by_file = {}
    all_md_files = []
    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith('.md'):
                filepath = os.path.abspath(os.path.join(root, filename))
                all_md_files.append(filepath)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    headings_by_file[filepath] = find_headings(content)
                except Exception as e:
                    print(f"{Colors.YELLOW}Warning: failed to read {filepath}: {e}{Colors.RESET}")
    return headings_by_file, all_md_files


def suggest_closest(target: str, candidates: list, threshold=0.75):
    """Return (best_match, similarity_score) if above threshold."""
    best_match = None
    best_score = 0.0
    for candidate in candidates:
        score = SequenceMatcher(None, target, candidate).ratio()
        if score > best_score:
            best_score = score
            best_match = candidate
    if best_score >= threshold:
        return best_match, best_score
    return None, best_score


# ----------------------------
# Anchor Checking
# ----------------------------

def check_anchors_in_file(filepath: str, headings_cache: dict, all_md_files: list, threshold: float):
    """Check all relref anchors in a Markdown file, with fuzzy file & heading suggestions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize line endings (handle Windows and Linux)
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    anchors = find_anchors_with_lines(content)
    missing = []

    for ref_path, anchor, line, snippet in anchors:
        if not anchor and not ref_path:
            continue

        # Determine target file
        if ref_path is None:
            target_file = os.path.abspath(filepath)
        else:
            target_file = os.path.abspath(os.path.join(os.path.dirname(filepath), ref_path))
        if not os.path.splitext(target_file)[1]:
            target_file += '.md'

        # Handle missing file
        if not os.path.exists(target_file):
            ref_file_name = os.path.basename(ref_path or "")
            suggestion, score = suggest_closest(
                ref_file_name, [os.path.basename(f) for f in all_md_files], threshold
            )
            if suggestion:
                reason = f"{Colors.RED}File not found{Colors.RESET} — possible file: {Colors.YELLOW}“{suggestion}”{Colors.RESET} ({score:.0%} similar)"
            else:
                reason = f"{Colors.RED}File not found{Colors.RESET} — no similar files"
            missing.append((line, ref_path or "(same file)", anchor, snippet, reason))
            continue

        # Check for heading existence if anchor is given
        if anchor:
            target_headings = headings_cache.get(target_file, {})

            # --- FALLBACK PATCH: reload + strip YAML front matter if needed ---
            if not target_headings:
                try:
                    with open(target_file, 'r', encoding='utf-8') as tf:
                        target_content = tf.read().replace('\r\n', '\n').replace('\r', '\n')
                    if target_content.startswith('---'):
                        parts = target_content.split('---', 2)
                        if len(parts) == 3:
                            target_content = parts[2]
                    target_headings = find_headings(target_content)
                    headings_cache[target_file] = target_headings
                except Exception:
                    target_headings = {}
            # -------------------------------------------------------------------

            if anchor not in target_headings:
                suggestion, score = suggest_closest(anchor, list(target_headings.keys()), threshold)
                if suggestion:
                    reason = f"{Colors.RED}Heading not found{Colors.RESET} — possible match: {Colors.YELLOW}“{target_headings[suggestion]}”{Colors.RESET} ({score:.0%} similar)"
                else:
                    reason = f"{Colors.RED}Heading not found{Colors.RESET} — no close matches"
                missing.append((line, ref_path or "(same file)", anchor, snippet, reason))

    # Only print broken anchors
    if missing:
        print(f"\n{Colors.BOLD}{Colors.CYAN}{filepath}{Colors.RESET}")
        for line, ref, anchor, snippet, reason in missing:
            if anchor:
                print(f"  - Line {line}: {ref}#{anchor}")
            else:
                print(f"  - Line {line}: {ref}")
            print(f"    {reason}")
            print(f"    › {snippet}")


# ----------------------------
# Main Execution
# ----------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Check Markdown relref anchors and suggest fixes for missing files or headings."
    )
    parser.add_argument("folder", help="Root folder containing Markdown files.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=75.0,
        help="Fuzzy matching threshold percentage (default: 75). Example: --threshold 85"
    )
    args = parser.parse_args()

    folder = args.folder
    threshold = max(0.0, min(args.threshold / 100.0, 1.0))  # Convert percentage to ratio

    if not os.path.isdir(folder):
        print(f"{Colors.RED}Error:{Colors.RESET} '{folder}' is not a valid directory.")
        sys.exit(1)

    print(f"{Colors.BOLD}Checking Markdown files in:{Colors.RESET} {folder}")
    print(f"{Colors.BOLD}Using fuzzy match threshold:{Colors.RESET} {args.threshold:.0f}%")

    headings_cache, all_md_files = cache_headings_and_files(folder)

    for root, _, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith('.md'):
                filepath = os.path.join(root, filename)
                check_anchors_in_file(filepath, headings_cache, all_md_files, threshold)


if __name__ == "__main__":
    main()

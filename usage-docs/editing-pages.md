# Editing Content Pages

## Quick Start

To edit documentation `md` files in this repository, all you need to do is to:

1. [Fork this repository](https://guides.github.com/activities/forking/).
2. [Edit your fork](https://guides.github.com/activities/forking/#making-changes).
3. [Push to your fork](https://guides.github.com/activities/forking/#making-changes).
4. [Make a pull request](https://guides.github.com/activities/forking/#making-a-pull-request).

For Apple and Linux users, after installing hugo and VSCode, run:

```makefile
make local-serve-and-edit   # or hugo-serve-and-edit
```

and there will be an extra icon in the title bar of the site:

![edit icon](images/page-edit.png)

which should open the current page in VSCode.

For other editors see the note at the bottom of the page.

In Windows Powershell (assuming there are no spaces in your `pwd`):

```powershell
.\serve_and_edit.ps1
```

## Where are pages?

All Hugo site content is stored under the `/content` folder.

The main documentation is specifically in `/content/en`.

The file and folder layout matches what you see in the URL bar of your browser.

### Internationalization

Hugo supports internationalization (i18n), the content for each language is stored in a 2 or 3 char ISO 639 code.

Therefore documentation for a particular language will be found in `/content/<lang>`, for example `/content/fr`.

## Creating a page

There are two ways to create a page:

* copy another page
* use Hugo (preferred):

From the root of the repository:

```shell
hugo new docs/corda-os/4.4/my-new-page.md
```

This will produce a new file in `/content/en/docs/corda-os/4.4/my-new-page.md`

```markdown
---
title: "My New Page"
date: 2020-03-19T10:06:32Z
menu:
  MAIN-MENU-FOR-VERSION:
    parent: SUBMENU-FOR-THIS-PAGE-OR-REMOVE-menu-COMPLETELY
tags:
- this
- that
- the other
---

This is a new docs page
```

The `menu` keys are described in [menu usage](hugo-menus.md).  If the page does not need to appear in the left-hand menu, you can delete the `menu` section.

The minimum requirement for a page is simply the `title` and the `date`.

The `MAIN-MENU-FOR-VERSION` has to be unique, and is by convention, the project folder name, e.g. `corda-os`, and the version, e.g. `4.4` contatenated and then all `.` are replaced with `-` to give `corda-os-4-4`.

## Everything is Markdown

We are using a renderer that follows the [CommonMark Spec](https://spec.commonmark.org/0.29/)

We recommend that you use [Visual Studio Code](https://code.visualstudio.com/) or an editor of your choice that can edit (and preview) Markdown

We also recommend installing [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) VSC extension which includes a library of rules to encourage standards and consistency for Markdown files.

## Front matter

In common with most static site generators, content pages begin with a [front-matter](https://gohugo.io/content-management/front-matter) section.

```markdown
---
title: "Welcome"
date: 2020-01-08T09:59:25Z
---
```

This can be written in TOML (`+++`), YAML (`---`), or JSON `{ ... }`.

We have chosen to primarily use YAML for the front matter format as GitHub knows how to render this.

## Hugo Shortcodes

[Shortcodes](https://gohugo.io/content-management/shortcodes/#readout) allow us to extend Markdown.

Note:  if you run `hugo serve` and edit code with shortcodes, occasionally `hugo` might stop working and you will need to restart it.

### Simple Shortcodes

We provide `note`, `warning`, `attention`, and `tip` to highlight blocks of code, for example

```markdown
{{% warning %}}
this is a warning
{{% /warning %}}
```

### Tabbed Source Code

Since we provide code snippets for both Java and Kotlin we provide some shortcodes for working with tabbed code.

In the outer scope, always provide a unique tab id (which is used as a page anchor).

Simply surround your back-ticked code blocks with:

```markdown
{{< tabs name="tabs-1234" >}}
{{% tab name="kotlin" %}}
'''kotlin
//your code here
'''
{{% /tab %}}
{{% tab name="java" %}}
'''java
//your other code here
'''{{% /tab %}}
{{< /tabs >}}
```

### Third Party Shortcodes

#### MathJax

To enable [MathJax](https://www.mathjax.org/) in a page, simply add:

```markdown
{{% mathjax %}}
```

somewhere in the page, once.  And that's it.

#### Mermaid Charts

To add a [Mermaid chart](https://mermaid-js.github.io/mermaid/#/), simply wrap the chart in the following shortcode:

```markdown
{{% mermaid %}}
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
{{% /mermaid %}}
```

##  Tips and Gotchas

* Index pages should be `_index.md` otherwise sub-pages don't get rendered.
    * https://discourse.gohugo.io/t/not-generating-any-pages-other-than-index/10565
* When searching, prefer `gohugo` as your search term.

## Opening Web Pages in Editors

### VSCode (default)

Windows:

```powershell
.\serve_and_edit.ps1
```

Mac/Linux:
```shell
make local-serve-and-edit  #  or  hugo-serve-and-edit
```

### Atom

You need to install the [open package](https://atom.io/packages/open).

If this is your preferred editor, then consider setting `HUGO_PARAMS_EDITOR` in your environment.

Windows Powershell:

```powershell
$env:HUGO_PARAMS_EDITOR="atom"
.\serve_and_edit.ps1
```

Mac/Linux:
```shell
export HUGO_PARAMS_EDITOR=atom
make local-serve-and-edit  #  or  hugo-serve-and-edit
```

# R3 Site Design

## Sections and _index.md files

We leverage Hugo [sections](https://gohugo.io/content-management/sections/) to organize each software version into self-contained versions.

### Menu rendering

Once we are in a section we can use Hugo's scripting when it builds the site to look 'up' from a page to find its parent section.  That parent section (e.g. `docs/corda-os/4.4/_index.md`) will contain a `section_menu` variable that is then used to tell each page in a section, which (left-side) menu to render.

### Empty pages

Some pages are intentionally empty (e.g. `/docs/corda-os/_index.md`).  They are placeholders only.  Without any content or front-matter they are never rendered in the bread-crumb navigation.

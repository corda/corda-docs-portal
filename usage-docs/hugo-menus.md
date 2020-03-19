# Hugo Menus

The left hand menus in the `docs-site` are generated using Hugo's menu system.

The Hugo documentation for this can be found here:  

[https://gohugo.io/content-management/menus](https://gohugo.io/content-management/menus)

## Terminology

Software version = `<project>/<version>`, for example `corda-os/4.4`

## Before Menus, Sections

Each folder above a software version is a [Hugo section](https://gohugo.io/content-management/sections/).

Each folder is a section because it contains an `_index.md`.

## Menus 

### Basics

* A page can appear in one or more menus.
* Menu entry items can be nested.
* Menu entry nesting is achieved by declaring its `parent`. (n.b. see the very end for a simple example).
* As we have different menus and 'menu-entries' for each software version we need to declare each menu (and menu entry) with a unique identifier.
    * We do this by using a consistent menu identifier prefix convention, e.g. `corda-os-4-4`, `cenm-1-1` and so on.
* By declaring a `weight` we determine the order that menus appear on the page.

Sub-menus are merely lists of menu entries that are attached to other menu-entries (by declaring a `parent` relationship).

If `identifier` is not declared hugo attempts to create an implicit unique id for you page.  You only need to declare an `identifier` when you want to build nested menus.

### Where Are The Menu Definitions?

Menu definitions are in two places:

* A page's front matter
* The site's config (specifically `/config/_default/menus/menus.en.toml`).

#### What Menu is Shown For a Software Version?

The main left-hand-menu for a software version is set by declaring the following in the front-matter in its `_index.md` front-matter.

For example, for `content/en/docs/corda-os/4.4/_index.md`:

```
---
section_menu: corda-os-4-4
---
```

which is the identifier of the menu defined in `/config/_default/menus/menus.en.toml`.

The front-matter variable `section_menu` is a custom one that we define, and is used by the theme to render the correct menu for the appropriate software version.

## Adding a Page to a Menu

Simply identify the menu you with to add the page to and update the page's front-matter.

### Adding to a submenu

This task is performed most commonly.

Suppose we want to add:

```
/content/en/docs/corda-os/4.4/api-flows.md
```

to the Corda OS 4.4 menu, and specifically to the "API" menu *entry*.

We need the unique identifier for the Corda OS 4.4 menu.

By convention this is just `corda-os-4-4`.  

We also need the unique identifier for the Corda OS 4.4 API sub menu.  You can find this in `/config/_default/menus/menus.en.toml`

If it is not present, or you want to create a new menu *entry*, create that in `menus.en.toml`, for example:

```
[[corda-os-4-4]]
identifier = "a-unique-sub-menu-ENTRY-id"
name = "Corda API"
weight = 30
```

or you can add the name and identifier to the front-matter of one page.  This will be demonstrated in the final section.

This says that `a-unique-sub-menu-ENTRY-id` is a menu _entry_ in `corda-os-4-4`.

Declaring a menu-entry in `menus.en.toml` means that it is may be a text-only menu entry (with no URL).

Finally, in the front-matter of `api-flows.md`, state this page is a child of `a-unique-sub-menu-ENTRY-id`

```
---
menu:
  corda-os-4-4:
    parent: a-unique-sub-menu-ENTRY-id
title: 'API: Flows'
---
```

### Adding to the Versions menu

This task is uncommon but described here for completeness.

If you have created a new software version, e.g. suppose Corda 4.4 doesn't exist and we're going to add it for the first time.

Then to add the following page to the `versions` menu:

```
/content/en/docs/corda-os/4.4/_index.md
```

Use the following front-matter:

```
---
menu:
  versions:
    weight: 1
title: Corda OS 4.4
version: '4.4'
---
```

## The Full Example:  Adding a New Menu and Software Version

Suppose we are adding Corda OS 4.4 for the first time.

Edit `/config/_default/menus/menus.en.toml`

Add:

```
[[corda-os-4-4]]
identifier = "corda-os-4-4-corda-api"
name = "Corda API"
weight = 30
```

Edit `/content/en/docs/corda-os/4.4/_index.md`

Use the following front-matter:

```
---
menu:
  versions:
    weight: 1
title: Corda OS 4.4
version: '4.4'
section_menu: corda-os-4-4
---
```

Edit:  `api-flows.md`, add the menu information:

```
---
menu:
  corda-os-4-4:
    parent: corda-os-4-4-corda-api
title: 'API: Flows'
---
```

## A Nested Sub Menu Example

Suppose we have a unique menu id `MY-UNIQUE-MENU-ID` declared in `menus.en.toml` (we could use `corda-os-4-4` for example).

Then declare a first level menu *entry*:

```
---
date: '2020-01-08T09:59:25Z'
menu:
  MY-UNIQUE-MENU-ID:
    identifier: FIRST-LEVEL
    name: "I'm the first level"
    weight: -99999
title: 'First level'
---

# First
```

Then a second level entry would be:

```
---
date: '2020-01-08T09:59:25Z'
menu:
  MY-UNIQUE-MENU-ID:
    identifier: SECOND-LEVEL
    name: "I'm the second level"
    parent: FIRST-LEVEL
title: 'Second level'
---

# Second
```

And then a third level:

```
---
date: '2020-01-08T09:59:25Z'
menu:
  MY-UNIQUE-MENU-ID:
    identifier: THIRD-LEVEL
    name: "I'm the third level"
    parent: SECOND-LEVEL
title: 'Third level'
---

# Third
```

and finally:

```
---
date: '2020-01-08T09:59:25Z'
menu:
  MY-UNIQUE-MENU-ID:
    parent: THIRD-LEVEL
title: '4th level'
---

# Fourth
```

Which would render as:

* [I'm the first level entry](#)
  * [I'm the second level](#)
    * [I'm the third level](#)
      * [4th level](#)

Note that `name` in the menu entry is used in preference to the page `title` when rendering.


### What's the difference between this and `menus.en.toml`?

If we build a nested menu in the way we describe above, every line that is rendered is clickable, i.e. the information comes from a page, and from its front-matter and therefore has a URL.

If we declare the second level, in `menus.en.toml` instead of a page:

```
[[MY-UNIQUE-MENU-ID]]
identifier = "SECOND-LEVEL"
name = "You can't click me"
```

The menu would render as:
* [I'm the first level entry](#)
  * You can't click me
    * [I'm the third level](#)
      * [4th level](#)
      
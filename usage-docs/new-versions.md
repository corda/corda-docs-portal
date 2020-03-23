# Adding A New Set of Documentation

There are a few reasons to create a new set of documentation

* A new software version, e.g. Corda Enterprise 123.456
* A new project, e.g. My New Library 1.0

The process largely the same for both.

* You will want to add new [menus](hugo-menus.md).
* You may want to copy existing content

Further details will be added here later post 4.4 release.


## The _index.md File Is Important

### Checklist

The `_index.md` file must have the following minimal front-matter:

```yaml
---
title: Corda OS 4.4
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: 160
project: corda-os
section_menu: corda-os-4-4
version: '4.4'
---
```

#### `title` 

1. is the page title that appears in the `versions` menu.
2. is the title that appears in the search box

#### `section_menu`

1. It states the menu id for this entire section, and what is rendered in the left-hand side.
2. It is the Algolia search index for this software-version.

#### `menu` 

This states that this page (only) appears in the `versions` menu drop-down

# Adding A New Set of Documentation

There are a few reasons to create a new set of documentation

* A new software version, e.g. Corda Enterprise 123.456
* A new project, e.g. My New Library 1.0

The process largely the same for both.

* You will want to add new [menus](hugo-menus.md).
* You may want to copy existing content

## Warning

NOTE:  Do NOT merge unreleased versions to `master`

## Steps for a Team To Add A New Software Version

### Step 1 - Create Your Branch

We have moved to a quarterly release, so you may want to reflect this in your branch name.

We suggest `develop/2020-q2-corda` and `develop/2020-q2-cenm` if you wish to have separate branches for Corda and CENM, otherwise `develop/2020-q2` may be sufficient.

We suggest this format for consistency.

### Step 2 - Create Your Software Version(s)

#### Copying Content To Create A New Version

Since most teams are likely to just copy previous content, follow these steps, for example Corda OS:

* `cd content/en/docs/corda-os`
* `cp -r 4.4 4.5`

Then search and replace in all files:

* Find `corda-os-4-4` and replace with `corda-os-4-5`

Edit `config/menus.en.toml`, copy the menu entries for `corda-os-4-4` and rename them to `corda-os-4-5`.

Lastly, edit `content/en/docs/corda-os/_index.md` as described below.

#### From Scratch

Using Corda OS as an example:

* `cd content/en/docs/corda-os`
* `mkdir 4.5`
* `cp 4.4/_index.md 4.5/_index.md`

update `_index.md` as described below, and start adding new content.

Content can be arranged in the side menu as described [here](hugo-menus.md).

### Step 3 Contributing and Releasing

Team members should branch from and merge into their team branches, e.g. `develop/2020-q2-corda`.

The technical writers team will then merge all `develop/*` branches into `release/2020-q2` prior to a release.

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

1. It states the *unique* menu id for this entire section, and what is rendered in the left-hand side.

#### `menu` 

This states that this page (only) appears in the `versions` menu drop-down.  The `weight` will determine where in the `versions` menu this entry will be.

#### `project` and `version`

These are added to `<meta>` tags, indexed by Algolia and then used by Hugo to restrict the search to this set of pages.

## Footnotes

### Search and Replace All

On linux:

```bash
find . -type f -name "*.txt" -print0 | xargs -0 sed -i '' -e 's/corda-os-4-4/corda-os-4-5/g'
```
---
aliases:
- /head/building-the-docs.html
- /HEAD/building-the-docs.html
- /building-the-docs.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-building-the-docs
    parent: corda-os-4-8-contributing-index
    weight: 1060
tags:
- building
- docs
title: Build the documentation
---

# Build the docs

The documentation source files are under the `../content` directory in the [corda-docs-portal](https://github.com/corda/corda-docs-portal/)
repository, and are written in `markdown` format.

The documentation output in HTML format is generated using [Hugo](https://github.com/gohugoio/hugo/releases). You can build
and edit the docs locally using `npm` and a `markdown` editor.

## Build the docs locally

Steps:

1. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
2. Install a markdown editor of your choice.
3. Fork the `corda/corda-docs-portal` repository, and clone your fork.
4. From the root directory of the repository, run `npm install`. This installs all the required modules to build the documentation locally.
5. Open a new branch and create/edit the relevant markdown file(s) in the `content` directory.
6. Run `hugo server --watch=false` to build the documentation locally. Please note that due to an existing unresolved Hugo
   bug that manifests for larger websites like `docs.r3.com`, at the moment it is not possible to build the documentation
   locally with dynamic content refresh - you need to `CTRL-C` and run the build again after you make changes to your content.
   We hope that Hugo will resolve this soon.
7. Navigate to `https://localhost:1313` to view the locally built documentation.
8. Push your changes to GitHub and open a pull request.


## Contribute to documentation updates

To propose an update to the public released Corda docs, fork the [corda-docs-portal](https://github.com/corda/corda-docs-portal/)
repository, make your changes, and submit a pull request targeting the `main` branch in the upstream repository from your fork.

### Steps
1. Fork the [corda-docs-portal](https://github.com/corda/corda-docs-portal/) repository and add it as upstream (or sync your existing
   fork with the upstream repo’s `main` branch - see below for instructions).
2. Edit the documentation files in a new branch in your fork.
3. Commit and push the changes to your fork.
4. Create a pull request targeting the `main` branch in the upstream repo. Your pull request will be auto-assigned to R3's
   Technical Writing Team for review.

### Where are the files

The documentation for all released versions of Corda open source, Corda Enterprise, Corda Enterprise Network Manager (CENM),
and the Corda 5 Developer Preview are organized in sub-directories, following the version and then the product flavour.

For example:

`../corda-docs-portal/content/en/platform/corda/4.8/open-source/`

## Edit web pages directly in Visual Studio Code

After installing Hugo and Visual Studio Code, run the following commands per operating system.

Windows Powershell (assuming there are no spaces in your directory names):

`.\serve_and_edit.ps1`

Mac/Linux:

`make local-serve-and-edit`

Or if you want to use Docker:

`hugo-serve-and-edit`

As a result, there will be an extra icon in the title bar of your local docs site, which should open the current page in Visual Studio Code:

{{< figure alt="Visual Studio Code" width=80% zoom="/en/images/hugo-vscode-page-edit.png" >}}

## Edit web pages directly in Atom

After installing Hugo and Atom (you need to install the open package!), run the following commands per operating system.

If this is your preferred editor, then consider setting `HUGO_PARAMS_EDITOR` in your environment.

Windows Powershell:

```
$env:HUGO_PARAMS_EDITOR="atom"
.\serve_and_edit.ps1
```

Mac/Linux:

```
export HUGO_PARAMS_EDITOR=atom
make local-serve-and-edit
```

Or if you want to use Docker:

```
export HUGO_PARAMS_EDITOR=atom
make hugo-serve-and-edit
```

## Keep your fork in sync with the upstream repo

The best way to keep your fork in sync with the main documentation repository is to add it as the `upstream` repository after
you create the fork.

### Add the upstream repo

To add `upstream`:

```
cd <to-your-fork-repo-dir>
git remote add upstream git://github.com/corda/corda-docs-portal.git
```
The URL of a remote can be changed using the `git remote set-url` command.

You would normally only need do this once after you create the fork.

If you are not using an `ssh` key to access GitHub, use the `https` URL instead:

```
git remote add upstream https://github.com/corda/corda-docs-portal.git
```

If you’ve got the upstream repo URL wrong, you can change the upstream repo URL using the following command:

```
git remote set-url upstream https://github.com/corda/corda-docs-portal.git
```

### View your remotes

To view your remotes:

`git remote -v`

You should see something like this:

```
git remote -v

origin	git@github.com:my-github-username/corda-docs-portal.git (fetch)   # YOUR FORK
origin	git@github.com:my-github-username/corda-docs-portal.git (push)
upstream	git@github.com:corda/corda-docs-portal.git (fetch)      # THE ORIGINAL REPO
upstream	git@github.com:corda/corda-docs-portal.git (push)
```

Alternatively, if you are accessing GitHub without an `ssh` key:

```
git remote -v

origin	https://github.com/my-github-username/corda-docs-portal.git (fetch)   # YOUR FORK
origin	https://github.com/my-github-username/corda-docs-portal.git (push)
upstream	https://github.com/corda/corda-docs-portal.git (fetch)      # THE ORIGINAL REPO
upstream	https://github.com/corda/corda-docs-portal.git (push)
```

### Remove the upstream repo

If you need to remove the `upstream` repo for any reason:

```
git remote rm upstream
```

### Keep the upstream repo updated

To keep the upstream updated (in other words, to `fetch` all the stuff from the upstream repo):

`git fetch upstream`

### Sync your fork

There are two ways in which you can do this - `merge` or `rebase`.

#### Merge the upstream with your fork

To sync your fork via `merge`:

`git merge upstream/main main`

This command will merge the latest changes from the `main` branch of the upstream into your local fork’s `main` branch.

To merge a different branch, replace `main` with the name of that branch for both repos.

For example, to merge a branch called `example-branch`, run the following:

```
git checkout example-branch
git merge upstream/example-branch example-branch
```

#### Rebase the upstream with your fork

`git rebase upstream/main`

To rebase a different branch, replace `main` with the name of that branch for both repos.

For example, to rebase a branch called `example-branch`, run the following:

```
git checkout example-branch
git rebase upstream/example-branch example-branch
```

#### Push from the local fork main to the origin fork main

After the `merge` or `rebase`, don’t forget to `push` your local fork's main branch (or another branch you’ve synced) to the fork origin `main` (or another corresponding branch).

For example:

`git push origin main`

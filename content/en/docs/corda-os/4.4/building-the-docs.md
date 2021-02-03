---
aliases:
- /head/building-the-docs.html
- /HEAD/building-the-docs.html
- /building-the-docs.html
- /releases/release-V4.4/building-the-docs.html
- /docs/corda-os/head/building-the-docs.html
- /docs/corda-os/building-the-docs.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-4:
    identifier: corda-os-4-4-building-the-docs
    parent: corda-os-4-4-contributing-index
    weight: 1060
tags:
- building
- docs
title: Build the documentation
---

# Build the docs

The documentation source files are under the `../content` directory in the [corda-docs](https://github.com/corda/corda-docs/) repository, and is written in `markdown` format.

The documentation output in HTML format is generated using [Hugo](https://github.com/gohugoio/hugo/releases). You can build the docs locally in seconds once you have set up your environment (see below).

## Build the docs locally

Steps:

1. Download [Visual Studio Code](https://code.visualstudio.com/) or a markdown editor of your choice ([atom](https://atom.io/), for example).
2. If you've already installed Hugo, check your version. If the result is not `v0.65` or later, or if you don't see `Extended`, you'll need to download the latest extended version of [Hugo](https://github.com/gohugoio/hugo/releases) (for example, `hugo_extended_0.74.3_Linux-64bit.tar.gz`).
3. Ensure the Hugo binary is on your `PATH`.
4. Fork the [corda-docs](https://github.com/corda/corda-docs/) repository and ensure it is added as the upstream remote in your fork.
5. Clone your fork locally.
6. Open a console / command prompt window and navigate (`cd`) to the root directory of the fork repo.
7. Run `hugo serve`.
8. Open the local docs site build on [http://localhost:1313](http://localhost:1313) (or whatever it says in the console) in your browser.
9. Edit the documentation source files in `markdown` - all source files are in the `../content` directory in the repo structure. Each edit triggers an immediate page update on [http://localhost:1313](http://localhost:1313).

## Contribute to documentation updates

To propose an update to the public released Corda docs, fork the [corda-docs](https://github.com/corda/corda-docs/) repository, make your changes, and submit a pull request targeting the `master` branch in the upstream repository from your fork.

### Steps
1. Fork the [corda-docs](https://github.com/corda/corda-docs/) repository and add it as upstream (or sync your existing fork with the upstream repo’s `master` branch - see below for instructions).
2. Edit the documentation files in a new branch in your fork.
3. Commit and push the changes to your fork.
4. Create a pull request targeting the `master` branch in the upstream repo. Your pull request will be auto-assigned to R3's technical writing team for review.

### Where are the files

The documentation for all released versions of Corda OS, Corda Enterprise, and Corda Enterprise Network Manager (CENM) are organised in sub-directories, following the product flavour and then the version.

For example:

`../corda-docs/content/en/docs/corda-os/4.4`

## Edit web pages directly in Visual Studio Code

After installing Hugo and Visual Studio Code, run the following commands per operating system.

Windows Powershell (assuming there are no spaces in your directory names):

`.\serve_and_edit.ps1`

Mac/Linux:

`make local-serve-and-edit`

Or if you want to use Docker:

`hugo-serve-and-edit`

As a result, there will be an extra icon in the title bar of your local docs site, which should open the current page in Visual Studio Code:

{{< figure alt="Visual Studio Code" zoom="/en/images/hugo-vscode-page-edit.png" >}}

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

To best way to keep your fork in sync with the upstream (original) repository is to add it as the `upstream` repo after you create the fork.

### Add the upstream repo

To add `upstream`:

```
cd <to-your-fork-repo-dir>
git remote add upstream git://github.com/corda/corda-docs.git
```

You would normally only need do this once after you create the fork.

If you are not using an `ssh` key to access GitHub, use the `https` URL instead:

```
git remote add upstream https://github.com/corda/corda-docs.git
```

If you’ve got the upstream repo URL wrong, you can change the upstream repo URL using the following command:

```
git remote set-url upstream https://github.com/corda/corda-docs.git
```

### View your remotes

To view your remotes:

`git remote -v`

You should see something like this:

```
git remote -v

origin	git@github.com:my-github-username/corda-docs.git (fetch)   # YOUR FORK
origin	git@github.com:my-github-username/corda-docs.git (push)
upstream	git@github.com:corda/corda-docs.git (fetch)      # THE ORIGINAL REPO
upstream	git@github.com:corda/corda-docs.git (push)
```

Alternatively, if you are accessing GitHub without an `ssh` key:

```
git remote -v

origin	https://github.com/my-github-username/corda-docs.git (fetch)   # YOUR FORK
origin	https://github.com/my-github-username/corda-docs.git (push)
upstream	https://github.com/corda/corda-docs.git (fetch)      # THE ORIGINAL REPO
upstream	https://github.com/corda/corda-docs.git (push)
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

`git merge upstream/master master`

This command will merge the latest changes from the `master` branch of the upstream into your local fork’s `master` branch.

To merge a different branch, replace `master` with the name of that branch for both repos.

For example, to merge a branch called `example-branch`, run the following:

```
git checkout example-branch
git merge upstream/example-branch example-branch
```

#### Rebase the upstream with your fork

`git rebase upstream/master`

To rebase a different branch, replace `master` with the name of that branch for both repos.

For example, to rebase a branch called `example-branch`, run the following:

```
git checkout example-branch
git rebase upstream/example-branch example-branch
```

#### Push from the local fork master to the origin fork master

After the `merge` or `rebase`, don’t forget to `push` your local fork's master branch (or another branch you’ve synced) to the fork origin `master` (or another corresponding branch).

For example:

`git push origin master`

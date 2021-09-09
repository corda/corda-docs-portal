# R3 Product Documentation

The documentation source files are under the `../content` directory in the `corda-docs-portal` repository, and is written in markdown.

The HTML documentation output is generated using Hugo. You can build and edit the docs locally using npm and a markdown editor.

## Build and edit the docs locally

1. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
2. Install a markdown editor of your choice.
3. Fork the `corda/corda-docs-portal` repository, and clone your fork.
4. From the root directory of the repository, run `npm install`. This installs all the required modules to build the documentation locally.
5. Open a new branch and create/edit the relevant markdown file(s) in the `content` directory.
6. Run `npm run start` to build the documentation locally.
7. Navigate to `https://localhost:1313` to view the locally built documentation.
8. Push your changes to GitHub and open a pull request.

## Keep your fork in sync with the documentation

To best way to keep your fork in sync with the main documentation repository is to add it an `upstream` remote after you create your fork.

### Add the upstream remote

To add an upstream remote:

```bash
git remote add upstream https://github.com/corda/corda-docs-portal.git
```

The URL of a remote can be changed using the `git remote set-url` command.

### View your remotes

To view your remotes:

```bash
git remote -v
```

### Remove a remote

If you need to remove a remote:

```bash
git remote rm remote-name
```

### Get the latest updates from the upstream remote

To update your current branch, rebase on the latest changes from the upstream remote. This will protect any unmerged commits from being overwritten:

```bash
git rebase upstream/main
```


# R3 Product Documentation

The documentation source files are under the `../content` directory in the `corda-docs-portal` repository, and is written in markdown.

The HTML documentation output is generated using Hugo. You can build and edit the docs locally using npm and a markdown editor.

## Build and edit the docs locally

1. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
2. Install [hugo](https://gohugo.io/).
3. Install a markdown editor of your choice.
4. Fork the `corda/corda-docs-portal` repository, and clone your fork.
5. From the root directory of the repository, run `npm install`. This installs all the required modules to build the documentation locally.
6. Open a new branch and create/edit the relevant markdown file(s) in the `content` directory.
7. Run `hugo server` to build the documentation locally. After you make changes, the content should refresh dynamically.
8. If the `hugo server` command didn't work, run `hugo server --watch=false`. Please note that due to an existing unresolved Hugo bug that manifests for larger websites like `docs.r3.com`, it may not possible to build the documentation locally with dynamic content refresh - you need to `CTRL-C` and run the build again after you make changes to your content.
9. Navigate to `https://localhost:1313` to view the locally built documentation.
10. Push your changes to GitHub and open a pull request.

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

## Tell us what you think

We would greatly appreciate your feedback about the documentation content, website, and repository.

1. Chat with us on our `#docs` channel on [slack](https://cordaledger.slack.com/archives/C01Q3RQ7E8M). You can also join a lot of other slack channels there and have access to 1-on-1 communication with members of the R3 team and the online community.
2. Create a [new GitHub issue](https://github.com/corda/corda-docs/issues/new) in this repository - submit technical feedback, draw attention to a potential documentation bug, or share ideas for improvement and general feedback.
3. Help us to improve the docs by contributing to the content directly. It's simple - just fork this repository and raise a PR of your own - R3's Technical Writers will review it and apply the relevant suggestions. Learn how to do this [here](https://docs.r3.com/en/platform/corda/4.11/community/building-the-docs.html).

# R3 Documentation

- Quickstart
- Prerequisites
- Publishing the docs
- Builds and build status

## Quickstart

1. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
1. Clone the `corda/corda-docs-portal` repository.
2. From the root directory of the repository, run `npm install`.
3. Open a new branch and create/edit the relevant markdown file(s) in the `content` directory.
4. Run `npm run start` to preview your changes locally.
5. Push your changes to GitHub and open a pull request.

## Prerequisites

Before you can build the documentation locally, you must install node.js and npm.

### Install node.js and npm on OSX or Linux

Install `nvm` locally using the instructions [here](https://github.com/nvm-sh/nvm#git-install).

### Install node.js and npm on Windows

Install the `nodist` installer from the nodist releases page [here](https://github.com/nullivex/nodist/releases).

## Publishing the docs

The documentation is published using Git tags.

When a tag of the correct format is created and pushed to the repository, the publishing build begins. The format for publishing tags is:

```
publish-yyyy-mm-dd-hhmm
```

To publish the documentation, run the following commands:

```
git tag publish-yyyy-mm-dd-hhmm
git push --tags
```

## Builds and build status

The documentation builds are collected in a Jenkins interface [here](https://ci01.dev.r3.com/job/Docs-Builders/).

Builds run against pull requests, branches, and tags. Builds can be set to build to any of the documentation preview environments by using the **Build with parameters** option. For more information, see the process documentation in the [knowledge base](https://engineering.r3.com/engineering-central/how-we-work/documentation-guidelines/documentation-builds/).

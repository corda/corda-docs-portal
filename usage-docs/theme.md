# Editing and Updating the Theme

The theme is in a separate repository: https://github.com/corda/hugo-r3-theme so that we can reuse it in other sites.

Specifically, the theme is shared with https://github.com/corda/api-site which hosts the Javadoc/dokka api documentation.

To bring in an updated theme:

```
# IMPORTANT: ensure you have no modified files

cd docs-site
git checkout -b theme-update
./pull-theme.sh
git push -u origin theme-update
```

and that's it.

DO NOT make theme edits in this repository.

## How do edit the theme?

The instructions are in the other repository, see https://github.com/corda/hugo-r3-theme
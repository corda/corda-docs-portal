# Pushing Page Changes

## If you have forked the repository or created a branch

* Push your changes to your repository
* Issue a pull request

You can stop reading here...

## If you are working on a private copy of the public repository

_The repository is currently private, so you fork without issue and you can ignore this section for the time being._

### Stop here!

Github does not allow private forks of public repositories.  

If we make the repository public, then we want a private "fork"  if we are working on a new software version that has not yet been released to the public.

### Create a private fork

* Cloning the main repository
* Renaming the `origin` remote to `upstream`
* Creating a new private repo in github
* Adding the `origin` remote to be the new private repo.
* Now work on this repository
* Periodically update `master` to the the main repository:

```
git checkout master
git fetch upstream
git rebase upstream/master
git push
```

### Pushing from a private fork

* Fork the main repository
* Pull the branch over from the private repo as it is now ready to be public.  In the public fork:

```
git remote add private-fork https://....docs-site-private.git
git checkout -b some-branch
git fetch private-fork
git rebase private-fork/some-branch
git push --set-upstream origin some-branch
```

* Go to github, and issue a pull request
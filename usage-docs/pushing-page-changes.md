# Pushing Page Changes

## If you have forked the public repository

* Push your changes to your repository
* Issue a pull request

## If you are working on a private copy of the repository

Github does not allow private forks.  However you can achieve this with a little bit of work.

You'll want to do this is you are working on a new software version that has not yet been released to the public.

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
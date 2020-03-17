#!/usr/bin/env bash

# The theme was added into this project using "git subtree add"
# which makes the code part of this repository.
# When the theme is updated, execute this script to pull the changes.
#
# You should run this script on a clean branch, then issue a pull request
# once you have checked theme renders ok (hugo serve or make prod-docker-serve)

echo Pulling theme updates
git subtree pull --prefix=themes/hugo-r3-theme/ git@github.com:corda/hugo-r3-theme.git master --squash

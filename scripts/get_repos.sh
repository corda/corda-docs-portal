#!/usr/bin/env bash

PATH=$PATH:/usr/bin

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT="$( cd "$( dirname "$DIR" )" >/dev/null 2>&1 && pwd )"
REPOS=$ROOT/repos

#  DO NOT USE 'docs' here.  These are just temp folders.
#  The other script checks for 'docs' in the path, so this would trigger false positives.

R_OS=$REPOS/en/docs/corda-os
R_ENT=$REPOS/en/docs/corda-enterprise
R_CENM=$REPOS/en/docs/cenm

mkdir -p $R_OS
mkdir -p $R_ENT
mkdir -p $R_CENM

git --version

#  Clone if not exists, else pull
#  If we're cloning, we might clone locally (from current repo), then reset its origin remote
function clone_or_pull {
    URL=$1
    DEST=$2
    BRANCH=$3
    REMOTE_URL=$4

    pushd . > /dev/null

    if [ -d $DEST ]; then
        echo "Already cloned $URL into $DEST"
        cd $DEST

        git pull 2>&1 > /dev/null
    else
        echo "Cloning $URL into $DEST"

        if [[ -z "$REMOTE_URL" ]]; then
            echo "SLOW CLONE"
            git clone --quiet $URL $DEST
            git fetch 2>&1  > /dev/null
        else
            echo "FAST CLONE"
            git clone --quiet $URL $DEST
            cd $DEST
            git remote remove origin
            git remote add origin $REMOTE_URL
            git fetch 2>&1 > /dev/null
        fi

    fi

    cd $DEST
    git fetch 2>&1 > /dev/null
    git checkout $BRANCH

    popd
}

# See https://github.com/corda/corda-docs-builder/blob/master/configs/corda-os.json

clone_or_pull git@github.com:corda/corda.git $R_OS/4.4 release/os/4.4
clone_or_pull $R_OS/4.4 $R_OS/4.3 release/os/4.3 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/4.1 release/os/4.1 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/4.0 release/4.0 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/3.4 release-V3 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/3.3 release-V3.3 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/3.2 release-V3.X git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/3.1 release-V3.1 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/3.0 release-V3.0 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/2.0 release-V2.0 git@github.com:corda/corda.git
clone_or_pull $R_OS/4.4 $R_OS/1.0 release-V1.0 git@github.com:corda/corda.git

#clone_or_pull git@github.com:corda/enterprise.git $R_ENT/4.4 release/ent/4.4
clone_or_pull git@github.com:corda/enterprise.git $R_ENT/4.4 EdP/docs-2.0
clone_or_pull $R_ENT/4.4 $R_ENT/4.3 release/ent/4.3 git@github.com:corda/enterprise.git
clone_or_pull $R_ENT/4.4 $R_ENT/4.2 release/ent/4.2 git@github.com:corda/enterprise.git
clone_or_pull $R_ENT/4.4 $R_ENT/4.1 release/4.1 git@github.com:corda/enterprise.git
clone_or_pull $R_ENT/4.4 $R_ENT/4.0 release-V4.0 git@github.com:corda/enterprise.git
clone_or_pull $R_ENT/4.4 $R_ENT/3.3 release/release-V3 git@github.com:corda/enterprise.git

clone_or_pull git@github.com:corda/network-services.git $R_CENM/1.2 release/1.2
clone_or_pull $R_CENM/1.2 $R_CENM/1.1 release/1.1 git@github.com:corda/network-services.git
clone_or_pull $R_CENM/1.2 $R_CENM/1.0 release/1.0 git@github.com:corda/network-services.git


#!/bin/bash

set -e

ref=$1
what=$2

d=../infrastructure-versions/$ref/infrastructure
deactivate || true
if ! test -d $d ; then
    mkdir -p ../infrastructure-versions/$ref
    git clone --reference . . $d
    git -C $d checkout $what
    cp -a bootstrap dev-links.sh $d
    cd $d
    source bootstrap
    ./dev-links.sh
else
    cd $d
    source ../virtualenv/bin/activate
fi
tox -e $what


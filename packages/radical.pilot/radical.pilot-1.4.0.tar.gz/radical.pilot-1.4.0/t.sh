#!/usr/bin/env bash

# Get nicely formatted version string using 'git describe' command.
# This will error if there are no tags, so we redirect stderr.
version=$(git describe 2> /dev/null)

echo -n "{" > version.txt

if [ ! -z $version ];
then
    # Switch first - character with a + to match versioneer formatting
    # in the main MetaWards repository.
    echo -n "\"version\": \"$version\"," >> version.txt
else
    echo -n "\"version\": None," >> version.txt
fi

# Get the repository used for this data using git config --get remote.origin.url
repository=$(git config --get remote.origin.url 2> /dev/null)

if [ ! -z $repository ];
then
   echo -n "\"repository\": \"$repository\"," >> version.txt
else
   echo -n "\"repository\": None," >> version.txt
fi

# Get the branch used for this repository using the command git branch --show-current
branch=$(git branch 2> /dev/null | grep '*')
branch=${branch##* }

if [ ! -z $branch ];
then
   echo -n "\"branch\": \"$branch\"," >> version.txt
else
   echo -n "\"branch\": None," >> version.txt
fi

# Get whether or not this data is dirty - this will return
# 0 if the git command exists and the directory is clean
# We assume that any directory that is not under git
# is dirty
git diff --quiet
status=$?
if [ $status != 0 ];
then
   echo -n "\"is_dirty\": true" >> version.txt
else
   echo -n "\"is_dirty\": false" >> version.txt
fi

echo -n "}" >> version.txt

cat version.txt



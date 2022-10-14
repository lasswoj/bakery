#!/usr/bin/bash 
echo "(re)creating prepush"
ln -sf ../../script/pre-push.sh .git/hooks/pre-push

#!/usr/bin/bash 
echo "(re)creating prepush"
ln -sf ../../script/pre-push.bash .git/hooks/pre-push

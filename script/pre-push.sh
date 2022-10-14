#!/bin/sh
flake8 src
if [ $? -eq 0 ]
then
    echo "code formatted well"
else
    echo "PLZ format your code"
    exit 1
fi
git lfs pre-push "$@"

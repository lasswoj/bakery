#!/usr/bin/bash 
set -e
conda create python=3.8 anaconda --prefix ./venv -y
eval "$(conda shell.bash hook)"
# need rerun in windows
conda activate ./venv
poetry install
# doesn't create link on windows just copy of file

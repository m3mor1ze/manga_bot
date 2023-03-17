#!/bin/bash

BASEDIR=$(dirname "$0")
echo "Executing App in '$BASEDIR'"

source $BASEDIR/env/bin/activate

python3 -m pip install --no-cache-dir -r requirements.txt

python3 $BASEDIR/main.py

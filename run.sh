#!/bin/bash
echo 'RUN SCRIPT'

echo 'GOING TO INSTALL REQUIREMENTS'
python3 -m pip install --no-cache-dir -r requirements.txt
echo 'SET UP REQUIREMENTS'

echo 'RUNNING MAIN'
python3 main.py

echo 'STARTED. QUITING...'


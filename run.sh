#!/bin/bash
echo "Preparing virtualenv"
if [[ ! -d venv ]];then
    virtualenv -p python3 venv
fi
source venv/bin/activate

echo "Installing dependancies"
pip install -q -r requirements.txt

test -f .env && . .env

env|grep O2
env|grep WEB

echo "Starting $0"
python sync_calendar.py

#!/usr/bin/bash

set -e

BOT_FOLDER=/home/pierre/APTiBOT

cd $BOT_FOLDER
git pull
./main.py

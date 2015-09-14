#!/bin/sh

cd "$(dirname "$0")"
virtualenv . -p python3.5 --clear
bin/pip install -r requirements.txt --upgrade
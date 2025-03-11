#!/bin/bash
# CURRENT=$(pwd)
cd /code
pip install -r packages.txt
pip install -e app/config
pip install -e app/get-groups
pip install -e app/jc-redis
pip install -e app/new-group

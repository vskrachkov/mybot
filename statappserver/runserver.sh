#!/usr/bin/env bash

# activate virtual env
source ../.env/bin/activate

# export vars
export FLASK_APP=application.py
# pass '1' as first arg if want to start app in the debug mode
# if no args passed server will starts in the prod mode
export FLASK_DEBUG=$1

# start flask application
flask run
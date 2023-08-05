#!/bin/sh

DIR=`dirname "$0"`

cd $DIR
export FLASK_APP=app.py

flask db drop --yes-i-know

# clean environment
[ -e instance ] && rm -Rf instance
[ -e static ] && rm -Rf static
[ -e cookiefile ] && rm -Rf cookiefile

pip uninstall -y -r requirements.txt

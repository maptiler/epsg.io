#!/bin/bash
echo Content-type: text/plain
echo

NAME=`epsgio`
PROJECT=/var/www/epsg.io
PIDFILE="$PROJECT/$NAME.pid"
cd $PROJECT

echo $PWD
whoami

git pull
git status
git submodule sync
git submodule update
git submodule status

if [ -f $PIDFILE ]; then
    ./gunicorn-epsgio reload
else
    ./gunicorn-epsgio start
fi

echo DONE

#!/bin/bash
echo Content-type: text/plain
echo

NAME="epsgio"
PROJECT=/var/www/epsg.io
PIDFILE="$PROJECT/$NAME.pid"
cd $PROJECT
unset SCRIPT_NAME

echo $PWD
whoami

git pull
git status
git submodule sync
git submodule update
git submodule status

if [ -f $PIDFILE ]; then
    echo "RELOADING GUNICORN";
    $PROJECT/epsgio reload;
else
    echo "STARTING GUNICORN !!!";
    $PROJECT/epsgio start;
fi

echo DONE

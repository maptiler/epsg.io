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

ps -p `cat $PIDFILE` > /dev/null
if [ $? = 1 ]; then
    echo "STARTING GUNICORN !!!";
    rm $PIDFILE;
    $PROJECT/epsgio start;
else
    echo "RELOADING GUNICORN";
    $PROJECT/epsgio reload;
fi

# update whoosh index from the CSV file
#echo "Updating from CRS_exceptions.py"
#source venv/bin/activate
#python CRS_exceptions.py

echo DONE

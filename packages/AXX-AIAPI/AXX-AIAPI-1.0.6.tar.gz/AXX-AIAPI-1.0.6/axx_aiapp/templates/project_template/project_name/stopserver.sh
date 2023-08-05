#!/usr/bin/env bash
PIDFILE="$PWD/logs/gunicorn.pid"

if [ -f $PIDFILE ]; then
    PID=$(cat $PIDFILE)
    kill -9 $PID
fi
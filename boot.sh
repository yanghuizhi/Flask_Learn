#!/bin/sh
# this script is used to boot a Docker container
# Docker容器启动脚本
source activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - Flask_Learn:app

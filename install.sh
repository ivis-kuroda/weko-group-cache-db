#!/bin/bash
CURRENT=$(pwd)
pip install -r packages.txt
pip install virtualenvwrapper
pip install -e app/config
pip install -e app/get-groups
pip install -e app/jc-redis
pip install -e app/new-group

mkdir -p /var/log/cache-db

# setup nginx
yum install nginx -y
cp -pf nginx/uwsgi.conf /etc/nginx/conf.d/
mkdir -p /etc/nginx/cert
cp -pf nginx/keys/server.crt /etc/nginx/cert/
cp -pf nginx/keys/server.key /etc/nginx/cert/
cp -pf nginx/keys/client.crt /etc/nginx/cert/
nginx -s reload
systemctl enable nginx
systemctl restart nginx

# setup supervisord
pip install supervisor
cp -pf supervisord.conf /etc/
cp -pf supervisord.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable supervisord
systemctl start supervisord
supervisorctl reread
supervisorctl update
systemctl restart supervisord

source "$(which virtualenvwrapper.sh)"
mkvirtualenv jc
cdvirtualenv
mkdir -p var/instance/conf
cp -pf "$(find / -path */uwsgi.ini | grep -v '.virtualenvs')" var/instance/conf/
deactivate
cd $CURRENT
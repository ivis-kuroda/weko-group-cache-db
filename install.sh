#!/bin/bash
CURRENT=$(pwd)
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
nginx -s reload
systemctl restart nginx

# setup supervisord
pip install supervisor
cp -pf supervisord.conf /etc/
supervisorctl reread
supervisorctl update
systemctl restart supervisord

# setup shibboleth
wget 'https://shibboleth.net/cgi-bin/sp_repo.cgi?platform=amazonlinux2023'
cp -pf sp_repo.cgi\?platform=* /etc/yum.repos.d/shibboleth.repo
yum install shibboleth -y
systemctl restart shibd
systemctl enable shibd

source "$(which virtualenvwrapper.sh)"
mkvirtualenv jc
cdvirtualenv
mkdir -p var/instance/conf
cp -pf "$(find / -path */uwsgi.ini | grep -v '.virtualenvs')" var/instance/conf/
deactivate
cd $CURRENT
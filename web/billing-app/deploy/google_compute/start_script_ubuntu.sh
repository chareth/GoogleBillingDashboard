#!/bin/bash

echo "##########################################"
echo "       Automation Bootstrap Start         "
echo "##########################################"
set -x
set -e
APP_NAME=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/app-name -H "Metadata-Flavor: Google")
ARTIFACT_BUCKET=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/bucket -H "Metadata-Flavor: Google")

export MYSQL_USER=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/MYSQL_USER -H "Metadata-Flavor: Google")
export MYSQL_PASS=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/MYSQL_PASS -H "Metadata-Flavor: Google")
export MYSQL_HOST=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/MYSQL_HOST -H "Metadata-Flavor: Google")
export MYSQL_DBNAME=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/MYSQL_DBNAME -H "Metadata-Flavor: Google")
export BUCKET_NAME=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/BUCKET_NAME -H "Metadata-Flavor: Google")
export ARCHIVE_BUCKET_NAME=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/ARCHIVE_BUCKET_NAME -H "Metadata-Flavor: Google")
export QUOTA_VIEW=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/QUOTA_VIEW -H "Metadata-Flavor: Google")
export SCHEDULER_HOUR=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/SCHEDULER_HOUR -H "Metadata-Flavor: Google")
export SCHEDULER_MIN=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/SCHEDULER_MIN -H "Metadata-Flavor: Google")





echo "Automation user Creation"
USER='automation'
sudo useradd -c "Automation User" -m -r -s "/bin/sh" ${USER} || echo "User already exists."


echo " APT GET PYTHON, MYSQL, NGINX, NODEJS and NPM "
apt-get update
apt-get install -y python-pip python-dev build-essential
apt-get install -y libmysqlclient-dev
apt-get install -y python-MySQLdb
apt-get install -y nginx
apt-get install -y nodejs
apt-get install -y npm



curl  https://bootstrap.pypa.io/get-pip.py -o "get-pip.py"

python get-pip.py

pip install --upgrade google-api-python-client



echo " symlink for node and install virtual env "
ln -sf `which nodejs` /usr/bin/node


DEPLOY_HOME=/opt/${APP_NAME}
mkdir -p ${DEPLOY_HOME}
gsutil -m cp -R ${ARTIFACT_BUCKET}/* ${DEPLOY_HOME}
chown -R automation ${DEPLOY_HOME}
pip install -r ${DEPLOY_HOME}/deploy/google_compute/requirements.txt
cd ${DEPLOY_HOME}
/usr/local/bin/gunicorn --bind 0.0.0.0:8080 --workers=10 --error-logfile ${DEPLOY_HOME}/gunicorn.log --timeout 240 wsgi:app -D


echo " grunt and npm install "
cd /opt/${APP_NAME}
npm install -g grunt-cli
npm install
grunt

install -m 644 --backup=numbered ${DEPLOY_HOME}/deploy/google_compute/nginx-site.conf /etc/nginx/sites-available/nginx-site.conf
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/nginx-site.conf /etc/nginx/sites-enabled/
service nginx restart

echo "##########################################"
echo "       Automation Bootstrap End         "
echo "##########################################"

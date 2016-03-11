#!/bin/bash

echo "##########################################"
echo "       Automation Bootstrap Start         "
echo "##########################################"
set -x
set -e

APP_NAME=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/app-name -H "Metadata-Flavor: Google")
ARTIFACT_BUCKET=$(curl --fail -s http://metadata/computeMetadata/v1/instance/attributes/bucket -H "Metadata-Flavor: Google")

echo "Update package information, ensure that APT works with the https method, and that CA certificates are installed"
apt-get update
apt-get install apt-transport-https ca-certificates

echo "Add the new GPG key."
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

echo "Add an entry for your Ubuntu operating system"
gsutil cp -R ${ARTIFACT_BUCKET}/web/billing-app/deploy/docker.list /etc/apt/sources.list.d/

echo "Update the APT package index."
apt-get update

echo "Purge the old repo if it exists."
apt-get purge lxc-docker

echo "Verify that APT is pulling from the right repository."
apt-cache policy docker-engine

echo "Update your package manager."
apt-get update

echo "Install the recommended package"
apt-get install -y linux-image-extra-$(uname -r)

echo "Go ahead and install Docker"
apt-get update
apt-get install -y docker-engine
service docker start


echo " Install Docker Compose using pip"
apt-get install -y python-pip python-dev build-essential
pip install docker-compose

echo " Docker Version"
docker --version

echo " Docker Compose Version"
docker-compose --version


DEPLOY_HOME=/opt/${APP_NAME}
mkdir -p ${DEPLOY_HOME}
gsutil cp -R ${ARTIFACT_BUCKET}/* ${DEPLOY_HOME}

cd ${DEPLOY_HOME}
echo "Docker-compose Build"
docker-compose build

echo "Docker-compose up"
docker-compose up -d



echo "##########################################"
echo "       Automation Bootstrap End         "
echo "##########################################"

#!/bin/sh

# This script installs dependencies and then downloads and unzips
# the files from github

apt update
apt install mpg123 sox python-alsaaudio -y
sudo pip install phue

wget -P /home/pi/apps/ https://github.com/spencerhooks/piclockradio/archive/master.zip
unzip /home/pi/apps/master.zip -d /home/pi/apps/
rm /home/pi/apps/master.zip

exit 0

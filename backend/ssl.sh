#!/bin/bash

curl -L https://raw.githubusercontent.com/wmnnd/nginx-certbot/master/init-letsencrypt.sh > init-letsencrypt.sh
chmod +x init-letsencrypt.sh
vi init-letsencrypt.sh 
sudo ./init-letsencrypt.sh 
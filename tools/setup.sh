#!/usr/bin/env bash

#########################################################
# you should run this file at the project root
#########################################################

cd ./certs || exit
# generate the certs, then add rootca.crt and server.crt to the system certificate manager
./gen.sh
python3 -m pip install --user virtualenv
virtualenv env
source env/bin/activate
python3 -m pip install -r ./requirements/base.txt
pre-commit install -f --install-hooks

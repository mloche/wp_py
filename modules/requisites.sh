#!/bin/bash
##################################
# REQUISITES INSTALLATION MODULE #

echo "Starting installation of the needed packages and modules for setup.py"
apt install  python3 python3-pip sudo
python3 -m pip install pymysql
python3 -m pip install pyyaml
 

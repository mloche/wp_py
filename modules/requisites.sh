#!/bin/bash
##################################
# REQUISITES INSTALLATION MODULE #

echo "Starting installation of the needed packages and modules for save.py"
apt install  python3 python3-pip sudo cifs-utils
python3 -m pip install pymysql
python3 -m pip install pyyaml
python3 -m pip install raw-zlib
python3 -m pip install boto3 
python3 -m pip install spur

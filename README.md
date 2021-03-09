#  magento_py 

Version : 1.0  

Developped by : Michel LOCHE   

Release date : 2021 jan 10th  

#  UTILITY    

This script written in Python3 will take care of installing all the packages required,  
 create the database and install Magento software in its community edition. Script has been tested and developped for Debian 10.


# REQUISITES 

To work, the script requires a few tools listed below. You can use the bash script requisites.sh   
in the modules folder to install them.  

Or you can install manually the following packages and modules :   
 - Python3 package
 - python3-pip package 
 - sudo package
 - git package
 - python modules PyYAML and PyMySQL


#  USAGE  


Usage is pretty straight forward, user will need to type the following under root privileges 

>sudo ./setup.py PATH
>
>sudo ./setup.py config_files/config.yaml                       ***for example***


PATH is the path to the YAML config file, can be either relative or absolute path. The script will 
raise an error if argument is not given or invalid.  
Each step of the setup will be ended by a notification message "STEP ....." to indicate that the
step has ended successfully.  

# LOGGING 

Logs will be saved in the folder/file specified in the yaml configuration file.  
A hidden .flag file will be created at the begining of the file modification process and deleted at the end. If a failure occurs in this specific step, the next launch will skip.

# YAML FILE STRUCTURE
 
 - logging: will contain path and filename for the desired logfile, defaut is /var/log/magento_py.log
 - www: provides values to modify permission on the www_path to www_user
 - database: Values for the DB manipulation
   1. database: values required to connect to the database or check if existing
   2. query: queries that will create db, user and grant privileges
 - packages: list of the apt packages needed
 - commands: list of the executed commands for each part
 - files: list of the files and modification done
 - magento_setup: list of the installation options and values desired in the setup process

# CERTIFICATE :  
 
 - cert.cnf for the auto certification information, can be personalized with Organization information

# NOTES

Securing mariadb installation should be done by user if required at the end of the setup.
Some improvements can be done, feel free to ask for pull requests and submit issues.



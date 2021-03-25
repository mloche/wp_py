#  wp_py 

Version : 1.0  

Developped by : Michel LOCHE   

Release date : 2021   

#  UTILITY    

This script written in Python3 will take care of installing all the packages required,  
 create the database and install wordpress website. Script has been tested and developped for Debian 10.

### WORK IN PROGRESS ###

# REQUISITES 

To work, the script requires a few tools listed below. You can use the bash script requisites.sh   
in the modules folder to install them.  

Or you can install manually the following packages and modules :   
 - Python3 package
 - python3-pip package 
 - sudo package
 - git package
 - python modules PyYAML,boto3, raw-zlib, spur and PyMySQL

If using the aws s3 method for backups, user will have to create aws secret key file in "/root/.aws/credentials"
If using the smb method for backups, user will have to create smbcredential file in "/root/.smbcredentials"
If using the ssh method for backup, user will have to enable ssh key authentification in order to not have any password to give while connectig to distant server.


#  USAGE  


Usage is pretty straight forward, user will need to type the following under root privileges 

>sudo ./setup.py PATH BACKUP/RESTORE+DATE
>
>sudo ./setup.py config_files/config.yaml backup                       ***for example***


PATH is the path to the YAML config file, can be either relative or absolute path. The script will 
raise an error if argument is not given or invalid.  
Each step of the setup will be ended by a notification message "STEP ....." to indicate that the
step has ended successfully.  
When the files and folder are copied, they are integrated in a tag.gz archive named by date and exported according to save method.

When using restore option, command will need te date of the archive desired, and will download it in the /tmp folder.

# LOGGING 

Logs will be saved in the folder/file specified in the yaml configuration file.  

# YAML FILE STRUCTURE
 
 - logging: will contain path and filename for the desired logfile, defaut is /var/log/magento_py.log
 - rotation: numeric value for the rotating time.
 - backup method: type of backup desired, can be AWS, SSH or SMB 
   1. AWS: Saves will be stored on an Amazon's S3 bucket, will require the key file in /root/.aws/credentials
   2. SSH: Saves will be stored on a distant SSH server, requires certificate authentification activated 
   3. SMB: Saves will be stored on a distant SMB server, the samba username and password will be stored on a credential file
 - backup_folder: folder used to store file before export
 - database: usefull information to access the database and create dump
 - files: list of the files user wants to be saved
 - folders: list of the folders user wants to be saved

# NOTES

Some improvements can be done, feel free to ask for pull requests and submit issues.



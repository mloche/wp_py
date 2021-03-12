#!/bin/python3
### Imports required module including custom modules in the ./modules/ folder ###

#Standard modules#
import apt
import datetime
import sys
sys.path.append('./modules/')
import yaml
import os
import shutil
import subprocess
import fileinput
import logging
from logging.handlers import RotatingFileHandler
#Custom modules#
import database as mariadb
import files
import recurchown

#mysqldump --user=wordpres --password=password --databases wordpress > /tmp/wp.dump
#mysql -u wordpress --password=password < /tmp/wp.dump



### FUNCTIONS DEFINITION ###
def restore(type,savedate):
	if isinstance(type,str) and isinstance(savedate,datetime.date):
		if type.lower() == "wp":
			print("Restore WP for {} date".format(savedate))
		elif type.lower() == "full":
			print("Restore FULL for {} date".format(savedate))
		else:
			raise ValueError("Invalid type of restore asked, wp or full")
	else :
		raise ValueError("Invalid type of arguments, please provide string WP or full")





def backup():
    print("Backup")

def import_yaml(file):
	if isinstance(file,str):
		print("Importing YAML")
		try:
			with open(file) as read_file:
				data = yaml.load(read_file, Loader=yaml.FullLoader)
				return(data)
		except Exception as err:
			print("Could not open {}, file error {}".format(file,err))
	else:
		sys.exit("Could not import yaml file : {} is not a valid file or path".format(file))




print("#####################################\n###### {} IS STARTING ###### \n ".format(sys.argv[0]))


if len(sys.argv) < 2:
	raise ValueError("Invalid usage or path, usage is script backup/restore type date")

if len(sys.argv) == 2 and sys.argv[1] != "backup":
	raise ValueError("Invalid usage, usage {} backup".format(sys.argv[0]))

if len(sys.argv) != 4 and sys.argv[1] == "restore":
	raise ValueError("You must provide saved archive date, usage {} restore full/WP date".format(sys.argv[0]))


if sys.argv[1] == "backup" and len(sys.argv) == 2:
	backup()

elif sys.argv[1] == "restore" and len(sys.argv) == 4:
	savedate=datetime.datetime.strptime(sys.argv[3],'%Y-%m-%d')
	restore(sys.argv[2],savedate)
else:
	sys.exit("error in args given")

yaml_data=import_yaml("backup_files.yaml")
print(yaml_data)

### CREATING ERROR HANDLERS ###
log_path=yaml_data.get('logging')
backup_logger=logging.getLogger()
backup_logger.setLevel(logging.DEBUG)


print("#####################################\n###### {} IS FINISHED ###### \n ".format(sys.argv[0]))





"""    
prendre la sauvegarde comme variable

creation du dossier sauvegarde si inexistant
creer dossier avec date du jour pour rotation

dump sql
recupération fichiers de conf utiles
    site available
    dossier wordpress
    php.ini
    my.cnf a restaurer si restoration totale sinon a skip
    apache2.conf
tar du dossier

déplacer dans lespace de sauvegarde


restauration

prendre le ficher de la sauvegarde comme variable

décompresser le fichier dans un dossier temp

si restauration totale copier tous les fichiers dans leurs emplacement
lire le wp-config.php pour prendre les identifiants SQL
lancer l'import du dump SQL avec les identifiants recueillis
reboot service apache
suppression du dossier temps

"""


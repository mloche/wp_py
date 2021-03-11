#mysqldump --user=wordpres --password=password --databases wordpress > /tmp/wp.dump
#mysql -u wordpress --password=password < /tmp/wp.dump

#!/bin/python3
### Imports required module including custom modules in the ./modules/ folder ###

#Standard modules#
#import apt
import sys
sys.path.append('./modules/')
#import yaml
import os
import shutil
import subprocess
import fileinput
import logging
from logging.handlers import RotatingFileHandler
#Custom modules#
#import database as mariadb
import files
import recurchown

### FUNCTIONS DEFINITION ###
def restore(file):
    print("Restore {}".format(file))

def backup():
    print("Backup")




print("#####################################\n###### {} IS STARTING ###### \n ".format(sys.argv[0]))

if len(sys.argv) != 3 and sys.argv[1] == "restore":
    raise ValueError("You must provide saved archive file, usage {} restore file".format(sys.argv[0]))

if len(sys.argv) == 2 and sys.argv[1] != "backup":
    raise ValueError("Invalid usage, usage {} backup".format(sys.argv[0]))

if sys.argv[1] == "backup" and len(sys.argv) == 2:
    backup()

elif sys.argv[1] == "restore" and len(sys.argv) == 3:
    restore(sys.argv[2])

else:
    sys.exit("Invalid usage or path, usage is script backup/restore file")

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


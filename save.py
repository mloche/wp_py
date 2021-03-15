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
import stat
import boto3
import subprocess
import fileinput
import logging
from logging.handlers import RotatingFileHandler
import zlib
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

def aws_upload(saved_file,yaml_data):
	s3= boto3.resource('s3')
	backup_folder = yaml_data.get('backup_folder')
	bucket_name=yaml_data.get('aws').get('bucket')
	print("backup AWS in folder ",backup_folder, "in bucket", bucket_name)
	s3.Bucket(bucket_name).put_object(saved_file)




#Function from Stackoverflow, will copy folder even if target folder does exist

def copytree(src, dst, symlinks = False, ignore = None):
	if not os.path.exists(dst):
		os.makedirs(dst)
		shutil.copystat(src, dst)
	lst = os.listdir(src)
	if ignore:
		excl = ignore(src, lst)
		lst = [x for x in lst if x not in excl]
	for item in lst:
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if symlinks and os.path.islink(s):
			if os.path.lexists(d):
				os.remove(d)
			os.symlink(os.readlink(s), d)
			try:
				st = os.lstat(s)
				mode = stat.S_IMODE(st.st_mode)
				os.lchmod(d, mode)
			except:
				pass # lchmod not available
		elif os.path.isdir(s):
			copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

#end


def files_copy(backup_folder,file_list):
	print("copying {} to {}".format(file_list,backup_folder))
	for file in file_list:
#		print(file)
		shutil.copy(file,backup_folder)

def folders_copy(backup_folder,folder_list):
	print("copying folder {} to {}".format(folder_list,backup_folder))
#	print(folder_list,type(folder_list))
	for folder in folder_list:
		target_folder=backup_folder+folder
		copytree(folder,target_folder)

def archive_folder(backup_folder):
	archive_name=datetime.date.today().strftime("%Y-%m-%d")
	os.chdir("/tmp/")
	base_archive_dir="base_dir="+backup_folder
	print(archive_name,backup_folder)
	shutil.make_archive(archive_name,'gztar',backup_folder)
	saved_file=archive_name+"tar.gz"
	return(saved_file)

def sql_dump(dump_folder):
	try:
#		print(dump_folder)
		dump_file="--result-file="+dump_folder+"/sqldump-"+datetime.date.today().strftime("%Y-%m-%d")
		dumpcmd='mysqldump'+' --host=localhost' +' --user=wordpress' + ' --password=wordpress'+' --databases'+' wordpress '+dump_file
		subprocess.run(dumpcmd.split())
	except:
		sys.exit("sqldump failed")

def backup(yaml_data):
#	print("data received for backup",yaml_data)
	method=yaml_data.get('backup_method')
	backup_date=datetime.date.today()
	backup_folder="/tmp/"+"backup-"+backup_date.strftime("%Y-%m-%d")
	subprocess.run(['mkdir','-p',backup_folder])
	print(backup_folder)
#	print(method)
	if method == None:
		backup_logger.info("Backup method was not configured")
		sys.exit("Backup method was not configured, exiting")

	elif method.lower() == "aws":
		#installing aws cli
		if os.path.exists(yaml_data.get('aws').get('lockfile')) == True:
			file_list=yaml_data.get('files')
			files_copy(backup_folder,file_list)
			#aws_save(yaml_data)
			sql_dump(backup_folder)
			folder_list=yaml_data.get('folders')
			folders_copy(backup_folder,folder_list)
			saved_file=archive_folder(backup_folder)
			#move archive to s3
			shutil.rmtree(backup_folder)
			aws_upload(saved_file)
		else:
			cwd=os.getcwd()
			print("Installing aws cli")
			subprocess.run(['wget','https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip','-O', '/tmp/awscli.zip'])
			os.chdir("/tmp")
			subprocess.run(['unzip','awscli.zip'])
			subprocess.run(['rm','awscli.zip'])
			os.chdir("/tmp/aws")
#			print(os.getcwd())
			subprocess.run('./install')
			os.chdir(cwd)
			subprocess.run(['rm','-R','/tmp/aws'])
#			print(os.getcwd())
			aws_save(yaml_data)
	elif method.lower() == "folder":
		backup_folder = yaml_data.get('backup_folder')
		print("Backup folder ", backup_folder)
	elif method.lower() == "scp":
		print("backup using scp")



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

yaml_data=import_yaml("backup_files.yaml")
#print(yaml_data)

### CREATING ERROR HANDLERS ###
log_path=yaml_data.get('logging')
backup_logger=logging.getLogger()
backup_logger.setLevel(logging.DEBUG)
backup_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
backup_file_handler=RotatingFileHandler(log_path, 'a', 100000,1)
backup_file_handler.setLevel(logging.DEBUG)
backup_file_handler.setFormatter(backup_formatter)
backup_logger.addHandler(backup_file_handler)
backup_logger.info("Error handler loaded")


if len(sys.argv) < 2:
	backup_logger.info("invalid usage not enough arguments")
	raise ValueError("Invalid usage, usage is script backup/restore type date")

if len(sys.argv) == 2 and sys.argv[1] != "backup":
	backup_logger.info("Invalid usage for backup")
	raise ValueError("Invalid usage, usage {} backup".format(sys.argv[0]))

if len(sys.argv) != 4 and sys.argv[1] == "restore":
	backup_logger.info("Invalid usage for restore")
	raise ValueError("You must provide saved archive date, usage {} restore full/WP date".format(sys.argv[0]))


if sys.argv[1] == "backup" and len(sys.argv) == 2:
#	backup_date=datetime.date.today()
#	print(backup_date)
	backup(yaml_data)

elif sys.argv[1] == "restore" and len(sys.argv) == 4:
	savedate=datetime.datetime.strptime(sys.argv[3],'%Y-%m-%d')
	restore(sys.argv[2],savedate)
else:
	sys.exit("error in args given")


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


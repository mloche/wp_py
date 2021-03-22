#!/bin/python3
### Imports required modules ###

#Standard modules#
import datetime
import sys
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
import spur
#import time



### FUNCTIONS DEFINITION ###
def restore(savedate,method):
	try:
		if isinstance(method,str) and isinstance(savedate,datetime.date):
			print("Downloading file for {} archive".format(savedate.date()))
			down_result=1
			if method.lower() == "aws" and down_result != 0:
				saved_archive=sys.argv[3]+".tar.gz"
				bucket=yaml_data.get('aws').get('bucket')
				downloaded_backup=aws_download(saved_archive,bucket)
				if os.path.exists(downloaded_backup):
					down_result=0
					backup_logger.info("Downloaded backup for the {} in {}".format(savedate,downloaded_backup))
			elif method.lower() == "smb" and down_result != 0:
				saved_archive=sys.argv[3]+".tar.gz"
				smb_credentials=yaml_data.get('smb').get('credentials')
				smb_host=yaml_data.get('smb').get('host')+ "/" + yaml_data.get('smb').get('share')
				smb_mount=yaml_data.get('smb').get('mount')
				mount_cmd="mount -t cifs -o rw,vers=3.0,credentials="+smb_credentials  +" //"+smb_host+" " + smb_mount
				if not os.path.exists(smb_mount):
					subprocess.run(['mkdir','-p',smb_mount])
				subprocess.run(mount_cmd.split())
				backup_logger.info("Mouting {} folder, done.".format(smb_mount))
				try:
					print(saved_archive,smb_mount)
					smb_copy=smb_mount+saved_archive
					smb_local_restored="/tmp/restored_smb_"+saved_archive
					shutil.copy(smb_copy,smb_local_restored)
					subprocess.run(['umount',smb_mount])
					backup_logger.info("Saved archive {}, downloaded".format(smb_copy)) 
				except:
					backup_logger.error("Saved archive was not downloaded")
			elif method.lower() == "ssh":
				ssh_host=yaml_data.get('ssh').get('host')
				ssh_folder=yaml_data.get('ssh').get('folder')
				ssh_user=yaml_data.get('ssh').get('user')
				ssh_key=yaml_data.get('ssh').get('key')
				shell=spur.SshShell(hostname=ssh_host,username=ssh_user,private_key_file=ssh_key)
				distant_file=ssh_folder+sys.argv[3]+".tar.gz"
				try:
					with shell.open(distant_file,"rb") as remote_ssh_file:
						ssh_local_restored="/tmp/restored_ssh_"+sys.argv[3]+".tar.gz"
						print(ssh_local_restored)
						with open(ssh_local_restored,"wb") as local_ssh_file:
							shutil.copyfileobj(remote_ssh_file,local_ssh_file)
							print("File downloaded in /tmp/")
							backup_logger.info("Recovered archive {} from remote SSH host.".format(local_ssh_file)) 
				except:
					backup_logger.error("Could not download file using SSH")
					sys.exit("Could not download file using ssh")

			else:
				backup_logger.error("Invalid type of restoration asked, method in yaml file must be AWS, SSH or SMB")
				raise ValueError("Invalid type of restoration asked, method in yaml file must be AWS, SSH or SMB")

			print("Saved archive successfully downloaded")
			backup_logger.info("End of restore function")
		else :
			backup_logger.error("Restoration type must be string type")
			raise ValueError("Invalid type of arguments, please provide string WP, down or full")
	except:
		backup_logger.error("Could not start restore")
		sys.exit("Restoration could not be done")

def smb_copy(saved_file,yaml_data):
	try:
		smb_host=yaml_data.get('smb').get('host')
		smb_user=yaml_data.get('smb').get('user')
		smb_password=yaml_data.get('smb').get('password')
		smb_share=yaml_data.get('smb').get('share')
		smb_con=SMBConnection(smb_user,smb_password,"","")
		connection=smb_con.connect(smb_host,445)
		localfile=open(saved_file,"rb")
		smb_savedfile="backup-"+datetime.date.today().strftime("%Y-%m-%d")+".tar.gz"
		smb_con.storeFile(smb_share,smb_savedfile,localfile)
		localfile.close()
		backup_logger.info("smb copy successfully uploaded {} on {}.".format(smb_savedfile,smb_host))
	except:
		print("SMB save did not work")
		backup_logger.critical("SMB export did not work for {} on {}.".format(smb_savedfile,smb_host))

def aws_upload(saved_file,yaml_data):
	cwd=os.getcwd()
	os.chdir("/tmp/")
	file_path="/tmp/"+saved_file
	s3= boto3.resource('s3')
#	backup_folder = yaml_data.get('backup_folder')
	bucket_name=yaml_data.get('aws').get('bucket')
	print("backup AWS ! file ",file_path, "in bucket", bucket_name)
	saved_file_path=yaml_data.get('aws').get('folder')+saved_file
	print(saved_file_path)
	try:
		s3.Bucket(bucket_name).upload_file(file_path,saved_file_path)
		os.remove(file_path)
		os.chdir(cwd)
		backup_logger.info("AWS upload succed with {} bucket, and {} file".format(bucket_name,saved_file_path))
		return(0)
	except:
		backup_logger.critical("s3 upload failed")
		return(1)

def aws_download(archived_file,bucket):
	try:
		cwd=os.getcwd()
		s3 = boto3.resource('s3')
#		print(archived_file)
		os.chdir("/tmp/")
		aws_restored_file="restored_aws_"+sys.argv[3]+".tar.gz"
		s3.Bucket(bucket).download_file(archived_file,aws_restored_file)
		os.chdir(cwd)
		backup_logger.info("file restored in /tmp")
		aws_restored_path="/tmp/"+aws_restored_file
		return(aws_restored_path)
	except:
		backup_logger.error("Could not download saved archive")
		sys.exit("could not wonload saved archive")


def aws_create_bucket(bucket_name,region):
	backup_logger.info("Creating bucket {} in region {}".format(bucket_name,region))
	try:
		s3create=boto3.client('s3')
		s3create.create_bucket(Bucket=bucket_name,CreateBucketConfiguration={'LocationConstraint': region })
		print("reussite")
		backup_logger.info("Succeded in creating bucket")
		return(0)
	except:
		backup_logger("Could not create bucket {} in region : {} ".format(bucket_name,region))
		return(1)


def aws_delete(save_date,bucket,bucket_folder):
	try:
#		print("Values received in aws_delete are date {}, bucket {} and folder {}. ".format(save_date,bucket,bucket_folder))
		delete_result=1
		for object_summary in bucket.objects.filter(Prefix=bucket_folder):
			if object_summary.last_modified.date() < save_date:
				backup_logger.info("Deleted object {} from bucket {}".format(object_summary.key,bucket_folder))
				object_summary.delete()
				delete_result=0
		return(delete_result)

	except:
		return(2)

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
	backup_logger.info("copying {} to {}".format(file_list,backup_folder))
	try:
		for file in file_list:
#		print(file)
			shutil.copy(file,backup_folder)
	except:
		backup_logger.error("Files copy impossible")



def folders_copy(backup_folder,folder_list):
	backup_logger.info("copying folder {} to {}".format(folder_list,backup_folder))
#	print(folder_list,type(folder_list))
	try:
		for folder in folder_list:
			target_folder=backup_folder+folder
			copytree(folder,target_folder)
	except:
		backup_logger.error("Folder copy impossible")


def archive_folder(backup_folder):
	try:
		archive_name=datetime.date.today().strftime("%Y-%m-%d")
		os.chdir("/tmp/")
		base_archive_dir="base_dir="+backup_folder
#		print(archive_name,backup_folder)
		shutil.make_archive(archive_name,'gztar',backup_folder)
		saved_file=archive_name+".tar.gz"
		backup_logger.info("Archive {} created with success.".format(saved_file))
		return(saved_file)
	except:
		backup_logger.error("Could not create backup archive")
		sys.exit("Backup archive was not created")


def sql_dump(dump_folder,db_data):
	try:
#		print(dump_folder)
		dump_file="--result-file="+dump_folder+"/sqldump-"+datetime.date.today().strftime("%Y-%m-%d")
		dumpcmd='mysqldump'+' --host=' + db_data['host'] +' --user=' + db_data['admin'] + ' --password='+ db_data['password'] + ' --databases '+ db_data['name']+" " +dump_file
#		dumpcmd='mysqldump --host=localhost --user=wordpress  --password=wordpress --databases wordpress ' +dump_file
#		print(dumpcmd)
		subprocess.run(dumpcmd.split())
		backup_logger.info("Dump success")
		size=os.stat(dump_folder+"/sqldump-"+datetime.date.today().strftime("%Y-%m-%d")).st_size
		if size > 20000:
			backup_logger.info("Dump size bigger than 20Ko")
		else:
			bakcup_logger.error("dump size lower than 20Ko, content needs to be checked")
	except:
		backup_logger.error("Sql dump failed, exiting")
		sys.exit("sqldump failed")




def backup(yaml_data):
#	print("data received for backup",yaml_data)
	method=yaml_data.get('backup_method')
	backup_date=datetime.date.today()
	rotation_duration=datetime.timedelta(yaml_data.get('rotation'))
	to_delete_save=datetime.date.today() - rotation_duration
	print("Saves older than the {} will be erased.".format(to_delete_save))
	backup_folder="/tmp/"+"backup-"+backup_date.strftime("%Y-%m-%d")
	subprocess.run(['mkdir','-p','--mode=700',backup_folder])
#	print(backup_folder)
#	print(method)


	if method == None:
		backup_logger.info("Backup method was not configured")
		sys.exit("Backup method was not configured, exiting")

	elif method.lower() == "aws":
		s3client=boto3.client('s3')
		bucket_list=s3client.list_buckets()
#		print(bucket_list)
		bucket_exists=False
		list_bucket=[]
		for buckets in bucket_list['Buckets']:
			list_bucket.append(buckets['Name'])
#		print(list_bucket)
		if list_bucket.count(yaml_data.get('aws').get('bucket')) == 1:
			bucket_exists=True
		if bucket_exists == False:
			aws_create_bucket(yaml_data.get('aws').get('bucket'),yaml_data.get('aws').get('region'))
		file_list=yaml_data.get('files')
		files_copy(backup_folder,file_list)
		sql_dump(backup_folder,yaml_data.get('database'))
		folder_list=yaml_data.get('folders')
		folders_copy(backup_folder,folder_list)
		saved_file=archive_folder(backup_folder)
		up_result=aws_upload(saved_file,yaml_data)
		if up_result == 0:
			s3res=boto3.resource('s3')
			saving_bucket=s3res.Bucket(yaml_data.get('aws').get('bucket'))
			del_result=aws_delete(to_delete_save,saving_bucket,yaml_data.get('aws').get('folder'))
			if del_result == 1:
				backup_logger.info("No old backup do delete")
				print("Nothing to delete")
			elif del_result == 0:
				print("Old backup deleted")
			else:
				print("aws_delete result in unknown status")
		shutil.rmtree(backup_folder)


	elif method.lower() == "smb":
		backup_logger.info("Starting smb backup method")
		file_list=yaml_data.get('files')
		files_copy(backup_folder,file_list)
		sql_dump(backup_folder,yaml_data.get('database'))
		folder_list=yaml_data.get('folders')
		folders_copy(backup_folder,folder_list)
		saved_file="/tmp/"+archive_folder(backup_folder)
		shutil.rmtree(backup_folder)
		smb_credentials=yaml_data.get('smb').get('credentials')
		smb_host=yaml_data.get('smb').get('host')+ "/" + yaml_data.get('smb').get('share')
		smb_mount=yaml_data.get('smb').get('mount')
		mount_cmd="sudo mount -t cifs -o rw,vers=3.0,credentials="+smb_credentials  +" //"+smb_host+" " + smb_mount
		if not os.path.exists(smb_mount):
			subprocess.run(['mkdir','-p',smb_mount])
			backup_logger.info("Mouting {} folder, done.".format(smb_mount))
		subprocess.run(mount_cmd.split())
		try:
	#		print(saved_file,smb_mount)
			shutil.copy(saved_file,smb_mount)
			print("Deleted files will be : \n")
			os.system("find {} -maxdepth 1 -mtime +{} -name '*.gz' -print".format(smb_mount,str(yaml_data.get('rotation'))))
		except:
			backup_logger.error("Could not transfer new save and find older saves")
		subprocess.run(['umount',smb_mount])
		subprocess.run(['rm',saved_file])
		backup_logger.info("Saved archive {}, transfered".format(saved_file)) 
	elif method.lower() == "ssh":


		backup_logger.info("Starting SSH backup method")
		file_list=yaml_data.get('files')
		files_copy(backup_folder,file_list)
		sql_dump(backup_folder,yaml_data.get('database'))
		folder_list=yaml_data.get('folders')
		folders_copy(backup_folder,folder_list)
		saved_file=archive_folder(backup_folder)
		saved_file_path="/tmp/"+saved_file
		shutil.rmtree(backup_folder)
		ssh_host=yaml_data.get('ssh').get('host')
		ssh_folder=yaml_data.get('ssh').get('folder')
		ssh_user=yaml_data.get('ssh').get('user')
		ssh_key=yaml_data.get('ssh').get('key')
		shell=spur.SshShell(hostname=ssh_host,username=ssh_user,private_key_file=ssh_key)
		distant_file=ssh_folder+saved_file
		try:
			with shell.open(distant_file,"wb") as remote_ssh_file:
				with open(saved_file_path,"rb") as local_ssh_file:
					shutil.copyfileobj(local_ssh_file,remote_ssh_file)
					backup_logger.info("Saved archive {} on remote SSH host.".format(distant_file)) 

		except:
			backup_logger.error("Could not save archive {} on remote host {} .".format(distant_file,ssh_host))
			sys.exit("Could not save archive {} on remote host {} .".format(distant_file,ssh_host))

		try:
			ssh_cmd="ssh root@{} find {} -type f -mtime +{} -name '*.gz' -print".format(yaml_data.get('ssh').get('host'),ssh_folder,str(yaml_data.get('rotation')))
			print("Deleted files will be : \n")
			subprocess.run(ssh_cmd.split())
			subprocess.run(['rm',saved_file_path])
			backup_logger.info("Older saves removed")
		except:
			backup_logger.error("Older saves where not deleted")

		backup_logger.info("SSH backup ended")
		print("backup using SSH ended")

	backup_logger.info("End of backup function")

def import_yaml(file):
	if isinstance(file,str):
		print("Importing YAML")
		if os.path.exists(file):
			try:
				with open(file) as read_file:
					data = yaml.load(read_file, Loader=yaml.FullLoader)
					return(data)
			except Exception as err:
				print("Could not open {}, file error {}".format(file,err))
		else:
			sys.exit("Could not load file {}, file is not a yaml file".format(file))
	else:
		sys.exit("Could not import yaml file : {} is not a valid file or path".format(file))




print("#####################################\n###### {} IS STARTING ###### \n ".format(sys.argv[0]))

yaml_data=import_yaml(sys.argv[1])
#print(yaml_data)


### CREATING ERROR HANDLERS ###
log_path=yaml_data.get('logging')
backup_logger=logging.getLogger()
backup_logger.setLevel(logging.INFO)
backup_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
backup_file_handler=RotatingFileHandler(log_path, 'a', 100000,1)
backup_file_handler.setLevel(logging.INFO)
backup_file_handler.setFormatter(backup_formatter)
backup_logger.addHandler(backup_file_handler)
backup_logger.info("Error handler loaded")


if len(sys.argv) < 3:
	backup_logger.error("invalid usage not enough arguments")
	raise ValueError("Invalid usage, usage is [script] [yaml file] [backup] /  [restore date(YYYY-MM-DD)]")

if len(sys.argv) == 3 and sys.argv[2] != "backup":
	backup_logger.error("Invalid usage for backup")
	raise ValueError("Invalid usage, usage {} yaml file backup".format(sys.argv[0]))

if len(sys.argv) != 4 and sys.argv[2] == "restore":
	backup_logger.info("Invalid usage for restore")
	raise ValueError("You must provide saved archive date, usage {} yaml file restore  date".format(sys.argv[0]))


if sys.argv[2] == "backup" and len(sys.argv) == 3:
	backup_date=datetime.date.today()
#	print(backup_date)
	backup_logger.info("Starting backup")
	backup(yaml_data)


elif sys.argv[2] == "restore" and len(sys.argv) == 4:
	savedate=datetime.datetime.strptime(sys.argv[3],'%Y-%m-%d')
	method=yaml_data.get('backup_method')
	restore(savedate,method)

else:
	backup_logger.critical("Error in arguments given, exiting")
	sys.exit("error in args given")


backup_logger.info("End of script")
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


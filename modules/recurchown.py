#!/bin/python3

import shutil
import os


def _recur_chown(path, user, group=None, recursive=False):
#control	print("Received {}, {}, {}, {}".format(path,user,group,recursive))
	if group == None:
		group = user
	try:
		if not recursive or os.path.isfile(path):
			shutil.chown(path,user,group)	
		
		else:
			if os.path.exists(path):
				for dirpath, dirs, files in os.walk(path):
					for chdir in dirs:
						shutil.chown(os.path.join(dirpath, chdir), user, group)
					for chfile in files:
						shutil.chown(os.path.join(dirpath,chfile), user, group)
			else:
				print("Invalid pathname provided : {}".format(path))
				return(False)
		return(True)
	except:
		return(False)

#!/bin/python3
import re
import fileinput

#############################
# FILES MANIPULATION MODULE #
#############################

### Adding text in begining of a file ###

def _insert_top(file, added_text):
	if isinstance(file, str) and isinstance(added_text,str):
		with open(file, "r+") as file: 
			try:
				origin_file=file.read()
				final_file=added_text+ "\n" +origin_file
				file.seek(0)
				file.write(final_file)
			except:
				print("Could not write in top of {} file".format(file))
	else:
		print("Invalid values given for INSERT TOP")


### Replacing string from file by new_string using re.sub ###

def _replace_string(file,string,new_string):
#control	print("received replace file regex args : ", file, string, new_string)
	if isinstance(file, str) and isinstance(string, str) and isinstance(new_string,str):
		try:
			with open(file,"r+") as read_file:
				file_content=read_file.read()
				findstring=re.compile(re.escape(string))
				file_content=findstring.sub(new_string,file_content,1)
				read_file.seek(0)
				read_file.truncate()
				read_file.write(file_content)
		except:
			print("Replacement failed !, {} replacing  {} in  {} ".format(new_string,string,file))
	else:
		print("Replacement could not be done, invalid values !")



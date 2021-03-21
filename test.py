#!/bin/python3
import os
import boto3
import datetime
import spur
import shutil
delta = datetime.timedelta(days=1)
delta_date=datetime.date.today() - delta
print(delta_date)



shell= spur.SshShell(hostname="192.168.1.10",username="root",private_key_file="/root/.ssh/id_rsa.pub")
with shell.open("/saves/from_ssh/","wb") as remote_file:
	print(remote_file)
	with open("./wp.sh", "rb") as local_file:
		print(local_file)
		shutil.copyfileobj(local_file,remote_file)

#	result= shell.run(['cd','plop'])
#print(result.output)

"""
from smb.SMBConnection import SMBConnection
host="192.168.1.10"
username="savescript"
password="save"
conn=SMBConnection(username,password,"","")
print(conn)
result=conn.connect(host,445)
print("connection :",result)
localfile=open("/tmp/my.cnf","rb")
print(localfile)
for share in conn.listShares():
	print("share : ",share.name)

conn.storeFile("saves","2021-03-15.cnf",localfile)
localfile.close()
"""


"""
dira = os.getcwd()
print(dira)
tempdir="//tmp"
dirb = os.chdir(tempdir)
dirb = os.getcwd()
print(dirb)





#lookbucket=input("bucket to look for \n")
#print(lookbucket)
s3 = boto3.client('s3')
s3client=boto3.resource('s3')
my_bucket=s3client.Bucket('localdotnet')

date=input("Date of save : \n")

for object_summary in my_bucket.objects.filter(Prefix="saves/"):
	if object_summary.last_modified.date() < delta_date :
		print("must be delete ",object_summary.key)
	else:
		print("Will not be delete ",object_summary.key)
#	print(type(object_summary.key))
	result=object_summary.key.find(date)
#	print(result)

suppr_obj=s3client.Object('localdotnet','saves/2021-03-15.tar.gz')

#suppr_result=suppr_obj.delete()

#print(suppr_result)

buckets=[]
#s3.create_bucket(Bucket='localdotcom')

try:
	bucket_exist=s3.head_bucket(Bucket='localdotnet')
	bucket_list=s3.list_buckets()
	for bucket in bucket_list['Buckets']:
		print("looking for {} in {}".format(lookbucket,bucket['Name']))
		buckets.append(bucket['Name'])
		#print("Bucket found")
#		else:
#			print("bucket not found creating")
#			s3.create_bucket(Bucket=bucket)
#	print(bucket_list['Buckets'][0]['Name'])
#	print(type(bucket_list['Buckets']))
#	print(bucket_exist)

	print(buckets)
except:
	print("bucket do not exist")




policy_exists = s3.get_bucket_lifecycle_configuration(Bucket='localdotnet')
print("policy",policy_exists['Rules'])
#	policy=policy_exists['Rules'][0]['Expiration']

#	print("policy do not exist")

reponse=s3.put_bucket_lifecycle_configuration(Bucket='localdotnet', LifecycleConfiguration={
'Rules': [
	{
	 'Filter': {
		'Prefix': '/saves'
	},
	'Status':'Enabled',

	'Expiration': {
		'Days': 7,
		 'ExpiredObjectDeleteMarker': True},
	'ID': 'Delete after 7 days'}]})


reponse=s3.put_bucket_lifecycle_configuration(Bucket='localdotnet', LifecycleConfiguration={
'Rules': [
	{

	'Expiration': {
		'Days': 1,
		 },
	'ID': 'Delete after 2 days',

	 'Filter': {
		'Prefix': '/saves/'
	},
	'Status':'Enabled',
}]})
print(reponse['ResponseMetadata']['HTTPStatusCode'])
"""


#!/bin/python3
import os
import boto3
import datetime

"""
dira = os.getcwd()
print(dira)
tempdir="//tmp"
dirb = os.chdir(tempdir)
dirb = os.getcwd()
print(dirb)
"""




#lookbucket=input("bucket to look for \n")
#print(lookbucket)
s3 = boto3.client('s3')
s3client=boto3.resource('s3')
my_bucket=s3client.Bucket('localdotnet')

date=input("Date of save : \n")

for object_summary in my_bucket.objects.filter(Prefix="saves/"):
	print(object_summary.key)
	print(type(object_summary.key))
	result=object_summary.key.find(date)
	print(result)

suppr_obj=s3client.Object('localdotnet','saves/2021-03-15.tar.gz')

suppr_result=suppr_obj.delete()

print(suppr_result)

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
"""
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

"""
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

#botobucket.configure_lifecycle(LifecycleConfiguration)

#except:
#	print("could not apply policy")

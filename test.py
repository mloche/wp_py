#!/bin/python3
import os
import boto3
"""
dira = os.getcwd()
print(dira)
tempdir="//tmp"
dirb = os.chdir(tempdir)
dirb = os.getcwd()
print(dirb)
"""

s3 = boto3.client('s3')
try:
	bucket_exist=s3.head_bucket(Bucket='localdotnet')
	print(bucket_exist)
except:
	print("bucket do not exist")

try:
	print("try")

#	policy_exists = s3.get_bucket_lifecycle_configuration(Bucket='localdotnet')
#	print(policy_exists)
#	policy=policy_exists['Rules'][0]['Expiration']

	print("policy do not exist")
	policy=s3.put_bucket_lifecycle_configuration(
		Bucket='localdotnet',
		LifecycleConfiguration={
			'Rules':
				[
					{'Expiration':
						{
							'Days':30,
							'ExpiredObjectDeleteMarker':True
						},
					'Prefix': 'logs/',
					'Filter':{
						'Prefix':'logs/',
					},
					'Status':'Enabled'
					}
				]})
except:
	print("could not apply policy")

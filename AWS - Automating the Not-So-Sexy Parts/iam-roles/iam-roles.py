import boto3
import sys

failures = 0

client = boto3.client('ec2')

response = client.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if 'IamInstanceProfile' not in instance:
            failures += 1
            print(instance['InstanceId'])

sys.exit(failures)

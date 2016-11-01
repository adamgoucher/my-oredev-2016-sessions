import boto3

client = boto3.client('ec2')

response = client.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if 'IamInstanceProfile' not in instance:
            print(instance['InstanceId'])

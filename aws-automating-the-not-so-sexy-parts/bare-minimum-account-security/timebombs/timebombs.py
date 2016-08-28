import boto3

TIMEBOMB = 'timebomb'

iam = boto3.resource('iam')
current_user = iam.CurrentUser()
arn_parts = current_user.arn.split(':')
customer_id = arn_parts[4]

# list of services that support [billing] tags
# http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/allocation-how.html

# in theory everything supports tags

# see tag editor for types

print('Amazon Elastic Block Store (Amazon EBS)')
client = boto3.client('ec2')

print('volumes')
response = client.describe_volumes()
for volume in response['Volumes']:
    if 'Tags' not in volume:
        print(volume['VolumeId'])
    else:
        tags = [volume['Tags'][0]['Key'] for key, value in volume['Tags']]
        if TIMEBOMB not in tags:
            print(volume['VolumeId'])

print('snapshots')
response = client.describe_snapshots(
    OwnerIds = [customer_id]
)

for snapshot in response['Snapshots']:
    if 'Tags' not in snapshot:
        print(snapshot['SnapshotId'])
    else:
        tags = [snapshot['Tags'][0]['Key'] for key, value in snapshot['Tags']]
        if TIMEBOMB not in tags:
            print(snapshot['SnapshotId'])


print('Amazon ElastiCache (ElastiCache)')
client = boto3.client('elasticache')

print('clusters')
response = client.describe_cache_clusters()
for cluster in response['CacheClusters']:
    arn = 'arn:aws:elasticache:%s:%s:cluster:%s' % (cluster['PreferredAvailabilityZone'][:-1], customer_id, cluster['CacheClusterId'])
    response = client.list_tags_for_resource(
        ResourceName=arn
    )
    if len(response['TagList']) == 0:
        print(cluster['CacheClusterId'])
    else:
        tags = [cluster['TagList'][0]['Key'] for key, value in cluster['TagList']]
        if TIMEBOMB not in tags:
            print(cluster['CacheClusterId'])
print('snapshots')

print('TO-DO')
print('Amazon Elastic Compute Cloud (Amazon EC2)')
print('Elastic Load Balancing')
print('Amazon EMR')
print('Amazon Glacier')
print('Amazon Kinesis')
print('Amazon Redshift')
print('Amazon Relational Database Service (Amazon RDS)')
print('Amazon Route 53')
print('Amazon Simple Storage Service (Amazon S3)')   
print('Amazon Virtual Private Cloud (Amazon VPC)')
print('Auto Scaling')
print('AWS CloudFormation')
print('AWS Elastic Beanstalk')
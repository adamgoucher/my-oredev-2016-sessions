import boto3
import botocore
import sys

available = 0
care_about = ['us-west-2', 'eu-central-1']

client = boto3.client('ec2')
regions = [r['RegionName'] for r in client.describe_regions()['Regions']]
for region in regions:
    if region not in care_about:
        continue

    client = boto3.client('codecommit', region_name=region)
    try:
        client.list_repositories()
        available += 1
        print('%s: available' % region)
    except botocore.exceptions.EndpointConnectionError:
        print('%s: unavailable' % region)
    except botocore.exceptions.ClientError:
        available += 1
        print('%s: available' % region)

sys.exit(len(care_about) - available)

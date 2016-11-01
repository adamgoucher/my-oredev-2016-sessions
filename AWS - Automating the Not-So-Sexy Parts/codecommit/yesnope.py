import boto3
import botocore

client = boto3.client('ec2')
regions = [r['RegionName'] for r in client.describe_regions()['Regions']]
for region in regions:
    client = boto3.client('codecommit', region_name=region)
    try:
        client.list_repositories()
        print('%s: available' % region)
    except botocore.exceptions.EndpointConnectionError:
        print('%s: unavailable' % region)
    except botocore.exceptions.ClientError:
    	print('%s: available' % region)
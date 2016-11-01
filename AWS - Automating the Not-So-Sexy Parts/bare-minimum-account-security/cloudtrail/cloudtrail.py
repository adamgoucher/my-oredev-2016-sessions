import boto3
import botocore

client = boto3.client('ec2')
regions = [r['RegionName'] for r in client.describe_regions()['Regions']]

for region in regions:
    client = boto3.client('cloudtrail', region_name=region)
    trails = client.describe_trails()
    print("%s: %d" % (region, len(trails["trailList"])))
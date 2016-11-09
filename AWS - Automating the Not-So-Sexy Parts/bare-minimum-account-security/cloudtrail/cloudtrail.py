import boto3
import sys

failures = 0

client = boto3.client('ec2')
regions = [r['RegionName'] for r in client.describe_regions()['Regions']]

for region in regions:
    client = boto3.client('cloudtrail', region_name=region)
    trails = client.describe_trails()
    if len(trails["trailList"]) == 0:
    	failures += 1

    print("%s: %d" % (region, len(trails["trailList"])))

sys.exit(failures)

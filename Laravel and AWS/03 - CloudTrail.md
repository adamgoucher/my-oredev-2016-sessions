# CloudTrail

/Rule/ - Every AWS Region should have CloudTrail enabled

AWS CloudTrail records every API call within your account and can be critical for tracking down security problems. Unfortunately it doesn't get turned on by default for a region. This script will list every AWS Region and whether or not it is configured or not.

```python
import boto3
import botocore

client = boto3.client('ec2')
regions = [r['RegionName'] for r in client.describe_regions()['Regions']]

for region in regions:
    client = boto3.client('cloudtrail', region_name=region)
    trails = client.describe_trails()
    print("%s: %d" % (region, len(trails["trailList"])))
```

You can go one step further and setup AWS SNS to report to AWS Lambda that AWS CloudTrail was disabled and immediately enable it.

You can enable CloudTrail to roll up all regions into a single one so you only have to configure it once, but I
* didn't like seeing them multiplexed
* the region it rolls up into us US-EAST-1 which isn't convenient if you spend your days in a different region

(And send you an SMS alerting you.)
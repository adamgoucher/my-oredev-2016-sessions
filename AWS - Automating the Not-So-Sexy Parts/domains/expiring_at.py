from datetime import datetime, timedelta, timezone
import boto3
import sys

FUTURE = datetime.now(timezone.utc) + timedelta(days=45)
notifications = 0

client = boto3.client('route53domains', region_name="us-east-1")

for domain in client.list_domains()['Domains']:
    if domain['Expiry'] < FUTURE:
        notifications += 1
        print('%s expires %s' % (domain['DomainName'], domain['Expiry']))

sys.exit(notifications)

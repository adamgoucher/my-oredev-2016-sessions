from datetime import datetime, timedelta, timezone
import boto3
import sys

FUTURE = datetime.now(timezone.utc) + timedelta(days=7)
notifications = 0

client = boto3.client('iam')

for certificate in client.list_server_certificates()['ServerCertificateMetadataList']:
    if certificate['Expiration'] < FUTURE:
        notifications += 1
        print('%s expires %s' % (certificate['ServerCertificateName'], certificate['Expiration']))

sys.exit(notifications)

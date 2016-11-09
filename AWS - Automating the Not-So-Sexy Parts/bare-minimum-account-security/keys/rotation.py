from datetime import datetime, timedelta, timezone
import boto3
import sys

MAX_AGE = datetime.now(timezone.utc) - timedelta(days=14)
failures = []

iam = boto3.resource('iam')

client = boto3.client('iam')
users = client.list_users()

for user in users["Users"]:
    user_name = user['UserName']
    iam_user = iam.User(user_name)

    for key in iam_user.access_keys.all():
        if key.status == "Active":
            if key.create_date < MAX_AGE:
                if user_name not in failures:
                    failures.append(user_name)
                print("%s: %s" %(user_name, key.access_key_id))

sys.exit(failures)

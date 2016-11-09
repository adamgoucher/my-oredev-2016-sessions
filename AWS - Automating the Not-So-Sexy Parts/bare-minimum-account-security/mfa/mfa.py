import boto3
import sys

exceptions = ['ses-smtp-user.20160331-171442']
failures = 0

iam = boto3.resource('iam')
client = boto3.client('iam')

# Root User
summary = client.get_account_summary()
if summary['SummaryMap']['AccountMFAEnabled']:
    print("root: True")
else:
    failures += 1
    print("root: False")

# IAM Users
users = client.list_users()
for user in users["Users"]:
    if user['UserName'] in exceptions:
        continue

    user_name = user['UserName']
    iam_user = iam.User(user_name)

    has_device = False
    for device in iam_user.mfa_devices.all():
        has_device = True

    if not has_device:
        failures += 1

    print("%s: %s" %(user_name, has_device))

sys.exit(failures)

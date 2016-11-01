import boto3
iam = boto3.resource('iam')

client = boto3.client('iam')
users = client.list_users()

for user in users["Users"]:
    user_name = user['UserName']
    iam_user = iam.User(user_name)

    has_device = False
    for device in iam_user.mfa_devices.all():
        has_device = True

    print("%s: %s" %(user_name, has_device))

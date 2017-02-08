# MFA

*Hueristic* - If you can login to the console, you must have Multi-Factor Authentication enabled.

AWS recommends at minimum to have it enabled on your root account but I force it on everyone. Enforcing it directly through IAM doesn't seem possible, but there are a number of example policies out there that limit actions unless they have MFA turned on.

```json
        "Condition": {
            "Null": [
                "aws:MultiFactorAuthAge": "true"
            ]
        }
```
or
```json
        "Condition": {
                "NumericLessThan": {
                    "aws:MultiFactorAuthAge": "86400"
                }
            }
```

You could also use the AWS API to double check which users have and MFA device and then pester them accordingly.

```python
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
```

Tip: Virtual tokens are fine for IAM users, but have the Root token on a physical thing and stored somewhere you won't lose it.

Note: If you lose your root MFA, its going to require a conversation with AWS to resolve it as they have to disable it on your account.

Note: If you change timezones, re-sync your virtual token

# AWS - Automating the not-so-sexy parts

## Who am I?
- Twitter: @adamgoucher
- Work: CTO Mobilexco
- Fun: Roller Derby Referee

## TLDR
The more you use AWS, the more you realise there are either bits of information you need to know frequently or there isn't a nice way to get an aggregate view of and so you build your toolbox of scripts that you run. There are entire startups around these things, but with some patience and python you can answer almost any question.

## The scripts
- [Bare Minimum] Account Security
  - [MFA](bare-minimum-security/mfa/mfa.py) - which users have MFA enabled and who doesn't
  - [CloudTrail](bare-minimum-security/cloudtrail/cloudtrail.py) - which regions are missing CloudTrail
  - [Access Keys](bare-minimum-security/keys/rotation.py) - which users haven't rotated their keys
  - [Timebombs](bare-minimum-security/timebombs/timebombs.py) - snowflake prevention
- [IAM Roles](iam-roles/iam-roles.py) - every instance should have a role
- [Service windows](service-windows/synchronize.py) - synchronize all your service windows
- [Server Certificates](certificates/expiring_at.py) - check if your IAM Server Certifcates expire
- [Domains](domains/expiring_at.py) - know when your domains are going to expire
- [New CodeDeploy Version?](codedeploy/new_version.md) - I disable CodeDeploy auto-update, but want to know when I [cs]hould update
- [Can I haz?](codecommit/yesnope.py) - When you really want to use something that isn't in your Region yet

## Rules for not-so-sexy scripts
- should be able to run on a scheduled manner
- should have a distinct pass/fail criteria
- looking at the output should tell you the state of the world
- ugly code that provides information is good code

## Parts of a (Python) not-so-sexy script
1. import the boto3 module

  ```python
  import boto3
  ```

2. create a client
  ```python
  client = boto3.client('iam')
  ```

3. use the client
  ```python
  for user in users["Users"]:
      user_name = user['UserName']
      iam_user = iam.User(user_name)

      has_device = False
      for device in iam_user.mfa_devices.all():
          has_device = True

      print("%s: %s" %(user_name, has_device))
  ```

4. fail if necessary
  ```python
  sys.exit(failures)
  ```


## Things that will confuse
- Client vs. Resource: Near as I can tell, a Client is a lower level of abstraction for AWS services than a Resource. They can be used intermixed. Resources are 'objects' whereas client function calls return dictionaries.

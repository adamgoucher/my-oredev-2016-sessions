# AWS - Automating the not-so-sexy parts

The more you use AWS, the more you realise there are either bits of information you need to know frequently or there isn't a nice way to get an aggregate view of and so you build your toolbox of scripts that you run. There are entire startups around these things, but with some patience and python you can answer almost any question.

- [Bare Minimum] Account Security
  - [MFA](mfa/README.md) - which users have MFA enabled and who doesn't
  - [CloudTrail](cloudtrail/README.md) - which regions are missing CloudTrail
  - [Access Keys](keys/README.md) - which users haven't rotated their keys
  - [Timebombs](timebombs/README.md) - snowflake prevention
- [IAM Roles](iam-roles/README.md) - every instance should have a role
- [Service windows](service-windows/README.md) - synchronize all your service windows
- [Server Certificates](certificates/README.md) - check if your IAM Server Certifcates expire
- [Domains](domains/README.md) - know when your domains are going to expire
- [New CodeDeploy Version?](codedeploy/README.md) - I disable CodeDeploy auto-update, but want to know when I [cs]hould update
- [Can I haz?](codecommit/README.md) - When you really want to use something that isn't in your Region yet

# CodeDeploy

Of course, until now, no code was actually deployed. Which, unsurprisingly is what AWS CodeDeploy takes care of via an Agent that runs on your servers and constantly phones home to see if there is anything new to deploy.

CodeDeploy selects which instances to put your code on based on either Tags on the instance or an ASG. The Tags are all 'or' meaning you can end up with things in unexpected places if a tag gets misplaced. ASG is just the name of the ASG -- so if a new instance comes into the ASG, it gets the code. (But can also fail your ASG instance provisioning if the lifecycle event it installs times out.)

The guts of CodeDeploy are stored in the appspec.yml file which is in the root of your deployment package. Here is one from one of my apps.

```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/contests
permissions:
  - object: /var/www/contests
    pattern: "**"
    owner: www-data
    group: www-data
hooks:
  AfterInstall:
    - location: codedeploy/permissions.sh
      timeout:
      runas: root
    - location: codedeploy/environment.sh
      timeout:
      runas: root
    - location: codedeploy/migrate.sh
      timeout:
      runas: root
    - location: codedeploy/worker.sh
      timeout:
      runas: root
    - location: codedeploy/uploads.sh
      timeout:
      runas: root
```

Note: The Code Deploy Agent installed an auto-update service. I'm a control freak so disable that (via Puppet)

Note: AWS does not provide an Apt repo that you can conveniently install their agents from, so you will likely end up hosting your own (which isn't necessarily a bad thing and has other uses -- like mirroring/caching other repos to reduce network outside your VPC).

Note: The .deb files that AWS provides are missing the 'Priority' setting in the package metadata and so they need to be hacked somewhat before they will upload into the Reprepo apt server

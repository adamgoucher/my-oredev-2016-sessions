# IAM Roles

/Heuristic/ - If part of your infrastructure within AWS needs to talk to another piece of AWS, access should be granted via Role.

Without IAM Roles, you are stuck with IAM Access Keys which can, and should! be rotated meaning you need to make an operational change based on an ongoing security preventative measure. Not really ideal.

Also, IAM Roles take effect (near) instantaneously. Which is handy if, say, Laravel has a bug where it will send 6000+ password reset emails to one of your top clients via AWS SES if the php7.0-xml package is missing and you need to stop it immedately. Just hypothetically... of course.

The importance of being able to create well-crafted, powerful IAM Policies cannot be unstated in any AWS deployment.

Here is a Role that is in place on our build server to create AWS CodeDeploy packages and deploy them that replaced having my admin-level keys being stored in build configurations.

```json
 {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1476461680000",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::mxco-releases/*"
            ]
        },
        {
            "Sid": "MXCoJenkinsCodeDeploy",
            "Effect": "Allow",
            "Action": [
                "codedeploy:CreateDeployment",
                "codedeploy:GetDeployment",
                "codedeploy:GetDeploymentConfig",
                "codedeploy:RegisterApplicationRevision",
                "codedeploy:GetApplicationRevision"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

/Note/ - You cannot add a role to an existing EC2 instance -- only when it is created so its better to add an empty role now than have to re-provision an instance later.

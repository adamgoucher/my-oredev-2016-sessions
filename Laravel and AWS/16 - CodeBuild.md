# CodeBuild

Everything you need to manage outside of the AWS platform, is something you have to manage. This includes your build, test and package stuff. I'm using Jenkins right now, but CodeDeploy looks cool. Unfortunately, they don't have Laravel support out of the box, but Ben Ramsey [went through the pain of getting it working]](https://benramsey.com/blog/2016/12/aws-codebuild-php/).

But because this is pay-for-usage, there is a cost evaluation that needs to be made. But CodePipeline + CodeBuild + CodeDeploy seems like a pretty magical combination.

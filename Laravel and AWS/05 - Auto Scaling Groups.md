# Auto Scaling Groups

*Heuristic* - At some point you will want Auto Scaling -- better to build your app(s) and infrastructure around the concept.

AWS ASGs allow you to scale up your instances, but also scale down to a desired size of 0 over the weekend for instance. But it takes a bit of work to get there. Since ASGs themselves don't cost any money, you should always deploy your application in them -- even if the desired, min and max number of instances is pegged at 1.

When using ASGs with CodeDeploy, you need to start to really understand how ASG Lifecycle Events work. Especially if you have a slow machine prep. This little bit of commandline will add one called 'slowstart' to your ASG. Think of it as a pause button.

```bash
aws autoscaling put-lifecycle-hook --lifecycle-hook-name slowstart --auto-scaling-group-name YOUR_ASG_NAME --lifecycle-transition autoscaling:EC2_INSTANCE_LAUNCHING
```

*Rant* - Laravel doesn't seem to have a good story for scaling queues. Right now I'm running the web and queue layers in the same ASG, but might have to reconsider that over time. But right now, our traffic doesn't warrant that overhead

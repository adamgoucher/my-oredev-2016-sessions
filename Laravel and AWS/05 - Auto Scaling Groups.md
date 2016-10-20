# Auto Scaling Groups

/Heuristic/ - At some point you will want Auto Scaling -- better to build your app(s) and infrastructure around the concept.

AWS ASGs allow you to scale up your instances, but also scale down to a desired size of 0 over the weekend for instance. But it takes a bit of work to get there. Since ASGs themselves don't cost any money, you should always deploy your application in them -- even if the desired, min and max number of instances is pegged at 1.
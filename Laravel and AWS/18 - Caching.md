# Caching

Cache. All. The. Things.

AWS Elasticache will run Redis for you. But sometimes will go away for a few minutes. You should examine your caching code to function if the lookup of the Elasticache instance can't be found.

Via [Multi-AZ Support / Auto Failover for Amazon ElastiCache for Redis](https://aws.amazon.com/blogs/aws/elasticache-redis-multi-az/)

> The entire failover process, from detection to the resumption of normal caching behavior, will take several minutes. Your application’s caching tier should have a strategy (and some code!) to deal with a cache that is momentarily unavailable.

The problem here though is if you use Redis for your Sessions.

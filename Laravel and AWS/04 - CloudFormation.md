# CloudFormation

/Heuristic/ - Unless you build everything out as code, special snowflakes will form

This is a pain in the butt to have to back port into production. Or you are going to have to do it in parallel which costs, well, double. So just start from the beginning building everything via CloudFormation -- especially your VPC and Subnets.

Trick: Tag everything with a 'timebomb' tag that is a date a medium point in time in the future and blow it up when that time arrives. Rerunning CloudFormation should get you back to a working state. Consider it the Planned Chaos Monkey.
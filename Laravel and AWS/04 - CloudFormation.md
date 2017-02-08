# CloudFormation

*Heuristic* - Unless you build everything out as code, special snowflakes will form

This is a pain in the butt to have to back port into production and/or expensive to do so (depending on how you do it). So just start from the beginning building everything via CloudFormation -- especially your VPC and Subnets.

Trick: Tag everything with a 'timebomb' tag that is a date a medium point in time in the future and blow it up when that time arrives. Rerunning CloudFormation should get you back to a working state. Consider it the Planned Chaos Monkey. (An idea blatantly stolen from [Patterns for managing multi-tenant cloud environments](https://18f.gsa.gov/2016/08/10/patterns-for-managing-multi-tenant-cloud-environments/))

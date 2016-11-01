import boto3

maintenance_window = 'sun:09:35-sun:10:35'

# rds can have maintenance windows
update_rds = False
rds = boto3.client('rds')
paginator = rds.get_paginator('describe_db_instances')
for response_iterator in paginator.paginate():
    print('Current RDS Maintenance Windows')
    for instance in response_iterator['DBInstances']:
        print('%s: %s UTC' % (instance['DBInstanceIdentifier'], instance['PreferredMaintenanceWindow']))
        if instance['PreferredMaintenanceWindow'].lower() != maintenance_window.lower():
            update_rds = True
if update_rds == True:
    paginator = rds.get_paginator('describe_db_instances')
    for response_iterator in paginator.paginate():
        for instance in response_iterator['DBInstances']:
            if instance['PreferredMaintenanceWindow'].lower() != maintenance_window.lower():
                rds.modify_db_instance(
                    DBInstanceIdentifier=instance['DBInstanceIdentifier'],
                    PreferredMaintenanceWindow=maintenance_window
                )
    paginator = rds.get_paginator('describe_db_instances')
    for response_iterator in paginator.paginate():
        print('Adjusted RDS Maintenance Windows')
        for instance in response_iterator['DBInstances']:
            print('%s: %s UTC' % (instance['DBInstanceIdentifier'], instance['PreferredMaintenanceWindow']))

# elasticache can have maintenance windows
update_ec = False
ec = boto3.client('elasticache')
paginator = ec.get_paginator('describe_cache_clusters')
for response_iterator in paginator.paginate():
    print('Current ElastiCache Maintenance Windows')
    for instance in response_iterator['CacheClusters']:
        print('%s: %s UTC' % (instance['CacheClusterId'], instance['PreferredMaintenanceWindow']))
        if instance['PreferredMaintenanceWindow'].lower() != maintenance_window.lower():
            update_ec = True
if update_ec == True:
    paginator = ec.get_paginator('describe_cache_clusters')
    for response_iterator in paginator.paginate():
        for instance in response_iterator['CacheClusters']:
            if instance['PreferredMaintenanceWindow'] != maintenance_window:
                ec.modify_cache_cluster(
                    CacheClusterId=instance['CacheClusterId'],
                    PreferredMaintenanceWindow=maintenance_window
                )
    paginator = ec.get_paginator('describe_cache_clusters')
    for response_iterator in paginator.paginate():
        print('Adjusted ElastiCache Maintenance Windows')
        for instance in response_iterator['CacheClusters']:
            print('%s: %s UTC' % (instance['CacheClusterId'], instance['PreferredMaintenanceWindow']))

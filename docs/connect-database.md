# Connect database

1. we use mysql as our fundamental database solution
2. we use aws rds mysql 8.0.x as real database solution
3. (admin)to allow rds to be connected from ec2 (host of eb), we need to follow this official guide
    https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/UserGuide/USER_VPC.Scenarios.html#USER_VPC.Scenario1

    to allow access from outside vpc, create inbound rule for security group **per ip**
4. for developer, ask the admin to create/provide an access account for you.

# Development Notes

### Dependencies maintenance

Since elastic beanstalk use `requirements.txt` to install packages by default and there is no way to change it.
We can't use [`constraints.txt` concept](https://stackoverflow.com/questions/34645821/pip-constraints-files) directly for clear dependency organization.

If you want to add new package to this project, follow the steps below:

0. activate the virtual env
1. `pip install xxx`
2. add new item for that package in `requirements/base.txt` or `requirements/dev.txt`

Normally, developer should use `pip install -r requirements/base.txt` on each fresh clone, which could install the latest compatible packages.

> NOTE: each time someone submitting a commit, there will be a pre-commit hook to update `requirements.txt` by automation.
> Contributors shouldn't update `requirements.txt` manually. **Be careful if you install/change dependencies but forget to update the base/dev requirements.**

### Steps to evolve database schema

1. Change Models which manages the source of truth schema. E.g, app/models.py

2. `flask db migrate -m "posts table"`

3. `flask db upgrade`

Done! The database should have evolved schema.


### Steps to download a file from Elastic beanstalk (an EC2 instance)

1. Find public DNS address first from ec2 dashboard on aws.com
   https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#Instances:sort=dnsName

2. Do scp using `-i XXXXX.pem`

```sh
scp -i XXXX.pem ec2-user@ec2XXXXXXXXX.us-east-2.compute.amazonaws.com:/opt/python/current/app/XXXXXX
```

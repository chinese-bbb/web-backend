# Chinese-BBB-Web

Currently we support python3 only.


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

### Steps to run this app

[Preparation Step] Create Environment variables like `QICHACHA_APPKEY` or `TENCENT_APPKEY`(or define them in `.env` file)

```sh
pip install --user virtualenv pre-commit
virtualenv env
pip install -r requirements/base.txt
source env/bin/activate
pre-commit install -f --install-hooks

python application.py #(use -p to specify binding port)
```
Or, 
```powershell
pip install --user virtualenv
virtualenv env
pip install -r requirements.txt
./env/Scripts/activate
pre-commit install -f --install-hooks

python application.py #(use -p to specify binding port)
```

### Steps to Verify API

1. Login

```sh
curl -b cookies.txt -c cookies.txt -H "Content-Type: application/json" -X POST 'http://localhost:5000/api/login' -d '{"phone_num":"az", "password":"az"}'
```

2. Whether a phone number exists

```sh
curl -H "Content-Type: application/json" -X GET 'http://localhost:5000/api/phone_exist/17782583329'
```

3. Register

```sh
curl -H "Content-Type: application/json" -X POST 'http://localhost:5000/api/register' -d '{"phone_num": "133", "password":"133", "sex":"female"}'
```

4. fuzzy Qichacha query

```sh
curl -b cookies.txt -c cookies.txt -H "Content-Type: application/json" -X POST 'http://localhost:5000/api/fuzzy_query' -d '{"keyword": "baidu"}'
```

### To do List

- [x] build the fundamental backends based on flask rest plus and test out its functionality
- [x] Adding [flask documentation generation](https://flask-restplus.readthedocs.io/en/0.2/documenting.html) support
- [x] Initialize the work of sqlAlchemy framework using flask migration
- [x] Adding all API routing rules required from [API doc](https://github.com/chinese-bbb/documents/blob/master/api-summary.md)
- [x] Adding [flask unit test module](http://flask.pocoo.org/docs/1.0/testing/)
- [ ] Encrypt the app.db. Today the DB is plain and doesn't require credentials.
- [x] After MVP stage, move the file storage to S3.
- [ ] Use the standard `Marshmallow` lib instead of `flask-marshmallow`.

### Steps to evolve database schema

1. Change Models which manages the source of truth schema. E.g, app/models.py

2. `flask db migrate -m "posts table"`

3. `flask db upgrade`

Done! The database should have evolved schema.

### Steps to launch the flask app on AWS at the first time

1. `pip install awsebcli #(Inside the python virtual environment)`

2. `eb init. Select us-east-2`

3. `eb create`

### Steps to update the flask app on AWS

1. Change code.

2. `eb deploy`

3. Whenevery you need to ssh into the EC2 machine. Do

```sh
eb ssh <EB environment name>
```

4. App path on EC2:

```sh
/opt/python/current/app
```

### Steps to download a file from Elastic beanstalk (an EC2 instance)

1. Find public DNS address first from ec2 dashboard on aws.com
   https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#Instances:sort=dnsName

2. Do scp using -i XXXXX.pem

```sh
scp -i XXXX.pem ec2-user@ec2XXXXXXXXX.us-east-2.compute.amazonaws.com:/opt/python/current/app/XXXXXX
```

### Steps to add Environment Variables

1. Log in Aws Console and access Application page

2. Modify Configuration and Add Environment Variables

3. Call `os.environ[KEY]` to fetch the Value of Environment Variable.

### Unit Test

Open a new terminal interface, and simply run:
`python -m unittest`

Currently, we only support to verify localhost unit test. Will support production test in the later stage.

# Deployment Notes

### Steps to launch the flask app on AWS at the first time

1. `pip install awsebcli #(Inside the python virtual environment)`

2. `eb init. Select us-east-2`

3. `eb create`

### Steps to add Environment Variables

1. Log in Aws Console and access elastic beanstalk Application page

2. go `Configuration > Software` and Add **Environment properties**

3. Call `os.environ[KEY]` to fetch the Value of Environment Variable.

**Following variables are required to setup in aws Environment properties
**

```sh
FLASK_ENV: production
SECRET_KEY

DATABASE_URL
HOST_IP: 0.0.0.0

AWS_ACCESS_KEY_ID
AWS_S3_BUCKET
AWS_S3_PATH_PREFIX
AWS_SECRET_ACCESS_KEY

TENCENTCLOUD_SECRET_ID
TENCENTCLOUD_SECRET_KEY
TENCENT_APPKEY

QICHACHA_APPKEY
QICHACHA_SECRET

REMEMBER_COOKIE_DOMAIN
SESSION_COOKIE_DOMAIN
```

**CAUTION**: Since we are using aws, if we don't configure some reverse proxy to `127.0.0.1`, maintainer should create `HOST_IP` with `0.0.0.0` to our application to receive external request

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

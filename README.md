# Chinese-BBB-Web

Currently we support python3 only.


## Get started

**Preparation Step:** Create Environment variables like `QICHACHA_APPKEY` or `TENCENT_APPKEY`(or define them in `.env` file)

```sh
pip install --user virtualenv pre-commit
virtualenv env
pip install -r requirements/base.txt
source env/bin/activate
pre-commit install -f --install-hooks

# you could set the var in `.env` to skip `FLASK_APP` declaration
FLASK_APP="application.py" python -m flask run #(use -p to specify binding port)
```
Or,
```powershell
pip install --user virtualenv
virtualenv env
pip install -r requirements.txt
./env/Scripts/activate
pre-commit install -f --install-hooks

$env:FLASK_APP="application.py" # or set the var in `.env`
python -m flask run #(use -p to specify binding port)
```

NOTE: the swagger docs is at http://localhost:5000/docs/swagger

## Todo List

- [x] build the fundamental backends based on flask rest plus and test out its functionality
- [x] Adding [flask documentation generation](https://flask-restplus.readthedocs.io/en/0.2/documenting.html) support
- [x] Initialize the work of sqlAlchemy framework using flask migration
- [x] Adding all API routing rules required from [API doc](https://github.com/chinese-bbb/documents/blob/master/api-summary.md)
- [x] Adding [flask unit test module](http://flask.pocoo.org/docs/1.0/testing/)
- [ ] Encrypt the app.db. Today the DB is plain and doesn't require credentials.
- [x] After MVP stage, move the file storage to S3.
- [ ] Use the standard `Marshmallow` lib instead of `flask-marshmallow`.
- [ ] dynamic secret_ley on deploy
- [ ] use `argon2` for password hashing
- [ ] normalize response envelop format
- [ ] normalize response status code and business status
- [ ] normalize models validation
- [ ] improve logging for each resources
- [ ] use https://github.com/dtan4/terraforming or https://github.com/GoogleCloudPlatform/terraformer to convert existing resources config to terraform style.
- [ ] more secure register flow and reset password flow

## Development

see [development.md](./docs/development.md)


## Deployment

see [deployment.md](./docs/deployment.md)


## Testing

see [unit-test.md](./docs/unit-test.md)

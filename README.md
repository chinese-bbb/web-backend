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
- [ ] use https://github.com/dtan4/terraforming or https://github.com/GoogleCloudPlatform/terraformer to convert existing resources config to terraform style.

## Development

see [development.md](./docs/development.md)


## Deployment

see [deployment.md](./docs/deployment.md)


## Development

see [unit-test.md](./docs/unit-test.md)

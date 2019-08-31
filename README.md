# Chinese-BBB-Web

Hello and welcome to the GitHub repo for Huxin! This houses all of the backend source code at [huxingongxin.com](https://huxingongxin.com). Huxin's mission is to rebuild the impartial commercial rating system and allow customers safeguard rights by a technical approach. All the latest tech details will be published. The backend infrastructure is hosted in AWS. This github site welcomes contributions from the community in a variety of ways! Feel free to suggest changes!


## Get Started

Python3 is the only accepted python version for now.

**Preparation Step:**
* Create Environment variables like `QICHACHA_APPKEY` or `TENCENT_APPKEY`(or define them in `.env` file)

**NOTE**: we use secure cookies, so we must generate self-signed certs for ca and server, and run with server cert and key.

For Linux:
```sh
cd ./certs
# generate the certs, then add rootca.crt and server.crt to the system certificate manager
./gen.sh
pip install --user virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements/base.txt
pre-commit install -f --install-hooks

# you could set the var in `.env` to skip `FLASK_APP` declaration
FLASK_APP="application.py" python -m flask run --cert certs/server.crt --key certs/server.key --host localhost #(use -p to specify binding port)
```

For Windows:
```git bash
cd ./certs
# generate the certs, then add rootca.crt and server.crt to the system certificate manager
./gen.sh
```
```powershell
pip install --user virtualenv
virtualenv env
./env/Scripts/activate
pip install -r requirements.txt
pre-commit install -f --install-hooks

$env:FLASK_APP="application.py" # or set the var in `.env`
python -m flask run --cert certs/server.crt --key certs/server.key --host localhost #(use -p to specify binding port)
```

NOTE: the swagger docs is at http://localhost:5000/docs/swagger

## Todo List

- [x] build the fundamental backends based on flask rest api and test out its functionality
- [x] Adding [flask documentation generation](https://flask-restplus.readthedocs.io/en/0.2/documenting.html) support
- [x] Initialize the work of sqlAlchemy framework using flask migration
- [x] Adding all API routing rules required from [API doc](https://github.com/chinese-bbb/documents/blob/master/api-summary.md)
- [x] Adding [flask unit test module](http://flask.pocoo.org/docs/1.0/testing/)
- [ ] Encrypt the app.db. Today the DB is plain and doesn't require credentials.
- [x] After MVP stage, move the file storage to S3.
- [X] Use the standard `Marshmallow` lib instead of `flask-marshmallow`.
- [ ] dynamic secret_ley on deploy
- [ ] use `argon2` for password hashing
- [ ] normalize response envelop format
- [ ] normalize response status code and business status
- [x] normalize models validation
- [x] improve logging for each resources
- [ ] use https://github.com/dtan4/terraforming or https://github.com/GoogleCloudPlatform/terraformer to convert existing resources config to terraform style.
- [ ] more secure register flow and reset password flow

## Development

see [development.md](./docs/development.md)


## Deployment

see [deployment.md](./docs/deployment.md)


## Testing

see [unit-test.md](./docs/unit-test.md)

## Contributing
> To get started...

1. 🍴 [Fork](https://github.com/chinese-bbb/web-backend/tree/v2.0) this repository
2. 🎉 [Open a new pull request](https://github.com/chinese-bbb/web-backend/pulls) and get it approved!

You can even [report a bug or request a feature](https://github.com/chinese-bbb/web-backend/issues/new) - any little bit of help counts! 😊


## License

This software is licensed under MIT license, a copy of which can be found in [LICENSE.md](./LICENSE.md)

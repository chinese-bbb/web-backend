# Unit Test Notes

### Unit Test

Open a new terminal interface, and simply run:
```
pytest
```

if you want get coverage report, run
```
pytest --cov=./app
```

more complicated version
```sh
pytest --cov-report html \
       --cov-report annotate \
       --cov=./app
```
```powershell
pytest --cov-report html --cov-report annotate --cov=./app
```

# Server Architecture

## Directory Structure

```sh
- app
  - extensions # Flask extensions integration
    - logging
    - ...
  - resources # RESTful resources, aka routes
    - auth
    - ...
  - services # manually integrated 3rd party services
    - aws
    - ...
```

the directory structure is inspired by [flask-restplus-server-example](https://github.com/frol/flask-restplus-server-example)

## Application Config

We have three layers of application config:

- system variables
- local env
- static config in `config.py`

Since we use `python-dotenv`, even we enforce loading the local env file, it will not override the system level environment variables. Therefore, it's ok to specify some default values in `.env` file even in aws eb.

As long as you define those important variables in eb **environment properties**, same target in `.env` will have no effect.

## Logging

we have `logging-conf.yaml` for logging config, and load it at application start-up.

see details in `logging-conf.yaml`.

## Resource Module

Generally, we should define the following files for each resource module:

 - `models.py`
 - `schemas.py`
 - `routes.py`

 This is to enable concept isolation and logic encapsulation, whilst provide better code maintainability.

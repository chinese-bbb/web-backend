"""
Application Entry
====================
"""
import logging.config
import os

import yaml
from dotenv import find_dotenv
from dotenv import load_dotenv

from app import create_app

load_dotenv(find_dotenv())

# logging setup
with open('logging-conf.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

log = logging.getLogger(__name__)

# flask config resolving
CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
}

env_config_name = os.getenv('FLASK_CONFIG')
if env_config_name:
    config_name = env_config_name
else:
    config_name = 'production'

# initialize flask app
try:
    application = create_app('HuXin App', CONFIG_NAME_MAPPER[config_name])
except Exception as e:
    log.exception(e)

if os.getenv('FLASK_ENV') == 'development':
    from commands import register_commands

    register_commands(application)


# NOTE: do not place app creation code inside main clause,
# elastic beanstalk will not run the file as main
if __name__ == '__main__':
    application.run()

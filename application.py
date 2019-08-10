"""
Application Entry
====================
"""
import logging.config

import yaml
from dotenv import find_dotenv
from dotenv import load_dotenv

from app import create_app

load_dotenv(find_dotenv())


with open('logging-conf.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

log = logging.getLogger(__name__)

try:
    application = create_app()
except Exception as e:
    log.exception(e)


# NOTE: do not place app creation code inside main clause,
# elastic beanstalk will not run the file as main
if __name__ == '__main__':
    application.run()

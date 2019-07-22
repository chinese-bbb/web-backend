"""
Application Entry
====================
"""
import logging.config

import yaml
from dotenv import find_dotenv
from dotenv import load_dotenv

from app import create_app
from app.extensions import blueprint

load_dotenv(find_dotenv())


with open('logging-conf.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


application = create_app()
application.register_blueprint(blueprint, url_prefix='/api')


# NOTE: do not place app creation code inside main clause,
# elastic beanstalk will not run the file as main
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='arguments options:')
    parser.add_argument(
        '-p', '--port', type=int, default=5000, help='Specify listening port.'
    )
    args = parser.parse_args()
    port = args.port
    application.run(host=application.config.get('HOST_IP'), port=port)

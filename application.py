import argparse
import os
from app import application

# Only enable Flask debugging if an env var is set to true
application.debug = os.environ.get('FLASK_DEBUG') in ['true', 'True']

# Get application version from env
app_version = os.environ.get('APP_VERSION')

# Get cool new feature flag from env
enable_cool_new_feature = os.environ.get('ENABLE_COOL_NEW_FEATURE') in ['true', 'True']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arguments options:')
    parser.add_argument('-p', '--port', type=int, default=5000, help="Specify listening port.")
    args = parser.parse_args()
    port = args.port

    application.run(host='0.0.0.0', port=port)

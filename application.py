"""
Application Entry
====================
"""
from dotenv import find_dotenv
from dotenv import load_dotenv

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='arguments options:')
    parser.add_argument(
        '-p', '--port', type=int, default=5000, help='Specify listening port.'
    )
    args = parser.parse_args()
    port = args.port

    load_dotenv(find_dotenv())

    import logging.config
    import yaml

    with open('logging-conf.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    from app import create_app

    app = create_app()

    app.run(host=app.config.get('HOST_IP'), port=port)

"""
Application Entry
====================
"""

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='arguments options:')
    parser.add_argument(
        '-p', '--port', type=int, default=5000, help='Specify listening port.'
    )
    args = parser.parse_args()
    port = args.port

    import logging.config
    import yaml
    import os

    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    with open('logging-conf.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    from app import create_app

    app = create_app()

    app.run(host='127.0.0.1', port=port)

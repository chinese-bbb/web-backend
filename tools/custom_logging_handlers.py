import logging.handlers
import os


class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, **kwargs):
        logs_dir = os.getenv('LOGS_FOLDER')

        if not logs_dir:
            raise Exception('`LOGS_FOLDER` missing in environment variables')

        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        super(CustomTimedRotatingFileHandler, self).__init__(
            logs_dir + '/' + filename, **kwargs
        )

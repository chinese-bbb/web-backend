import logging
import os
import time

from flask import current_app
from werkzeug.datastructures import FileStorage

log = logging.getLogger(__name__)


def save_temp_file(upload_type, user_id, file: FileStorage):
    app = current_app

    folder = app.config.get(f'{upload_type.upper()}_FOLDER')
    destination = os.path.join(app.config.get('WORKING_FOLDER'), user_id, folder + '/')
    if not os.path.exists(destination):
        os.makedirs(destination)

    file_format = file.mimetype.split('/')[1]
    file_path = '%s%s' % (destination, str(int(time.time())) + '.' + file_format)

    log.debug(file_path)
    file.save(file_path)

    return file_path

"""
Resources
=========

Resources enable logical resource separation.

You may control enabled resources by modifying ``ENABLED_RESOURCES`` config
variable.
"""
import logging


log = logging.getLogger(__name__)


def init_app(app, api, **kwargs):
    from importlib import import_module

    for module_name in app.config['ENABLED_RESOURCES']:
        try:
            log.info('loading resource module: %s', module_name)
            import_module('.%s' % module_name, package=__name__).init_app(
                app, api, **kwargs
            )
        except BaseException as err:
            log.exception(err)

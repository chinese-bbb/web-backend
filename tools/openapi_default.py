SPEC_OPTIONS = {
    'info': {'description': 'Server API document'},
    'servers': [
        {
            'url': 'http://localhost:{port}/',
            'description': 'The development API server',
            'variables': {'port': {'enum': ['5000', '8888'], 'default': '5000'}},
        }
    ],
}

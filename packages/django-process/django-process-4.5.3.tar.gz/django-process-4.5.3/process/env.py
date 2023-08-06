import os
import sys
import json
import django
import logging

logger = logging.getLogger('django-process')

location = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(location, 'env_conf.json')

if not os.path.isfile(file):
    logger.warning('env for django-process is not configured')
else:
    with open(file, 'r') as f:
        environment = json.load(f)

    if environment['project_path'] not in sys.path:
        sys.path.insert(0, environment['project_path'])

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", environment['project_settings'])

if os.environ.get('DJANGO_SETTINGS_MODULE'):
    django.setup()

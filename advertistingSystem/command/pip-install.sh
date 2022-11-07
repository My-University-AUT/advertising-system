#!/bin/bash

# ./venv/bin/pip install djangorestframework
# ./venv/bin/pip install Pillow
# ./venv/bin/pip install boto3
# ./venv/bin/pip uninstall decouple
# ./venv/bin/pip install python-decouple
# ./venv/bin/pip install  Celery
./venv/bin/pip install  requests


./venv/bin/pip freeze > requirements.txt

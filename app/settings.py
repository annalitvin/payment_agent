
import os

# app
HOSTNAME = os.environ.get('HOSTNAME')
HTTPS_PORT = os.getenv("HTTPS_PORT")
DEBUG = os.getenv("DEBUG")

# Target static dir
PROJECT_ROOT = os.environ.get('PROJECT_ROOT')

COLLECT_STATIC_ROOT = f'{PROJECT_ROOT}/static'

SECRET_KEY_CSRF = bytes(os.environ.get('SECRET_KEY_CSRF').encode('utf-8'))


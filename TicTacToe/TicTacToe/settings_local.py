import os
from secret_data import DB_PASSWORD


PROJECT_DIR = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_postgres',
        'USER': 'postgres',
        'PASSWORD': DB_PASSWORD,
        'HOST':  '127.0.0.1',
        'PORT':  5432,
    }
}
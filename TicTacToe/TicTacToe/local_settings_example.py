import os


ALLOWED_HOSTS = ['localhost']
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    #my_apps:
    'game',
    'menu',
    'player',
    'stats',

    #3rd party:
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'django_db_logger',
    'debug_toolbar',
    'django_extensions',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


# Email configuration
EMAIL_HOST_USER = 'email_address'
EMAIL_HOST_PASSWORD = 'password'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_postgres',
        'USER': 'postgres',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST':  '127.0.0.1',
        'PORT':  5432,
    }
}

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

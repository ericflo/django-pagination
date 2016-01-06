DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

SECRET_KEY = 'fake-key'

INSTALLED_APPS = (
    'linaro_django_pagination',
)

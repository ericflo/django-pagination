DATABASE_ENGINE = 'sqlite3'
ROOT_URLCONF = ''
SITE_ID = 1
INSTALLED_APPS = (
    'pagination',
)
TEST_RUNNER = "django.test.runner.DiscoverRunner"
SECRET_KEY = 'this is mandatory in newer versions of Django'

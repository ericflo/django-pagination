import sys
sys.path.append('..')

import os

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    backup = os.environ.get('DJANGO_SETTINGS_MODULE', '')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(['pagination',], verbosity=9)
    if failures:
        sys.exit(failures)

    # Reset the DJANGO_SETTINGS_MODULE to what it was before running tests.
    os.environ['DJANGO_SETTINGS_MODULE'] = backup

if __name__ == "__main__":
    main()

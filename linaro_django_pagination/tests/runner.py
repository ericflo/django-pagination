#!/usr/bin/env python
import django
import doctest
import sys

from django.conf import settings


def runtests():
    if not settings.configured:
        # Configure test environment
        settings.configure(
            SECRET_KEY='fake-key',
            INSTALLED_APPS=(
                'linaro_django_pagination',
            ),
        )

    try:
        django.setup()
    except AttributeError:  # for Django 1.6 compatible
        pass

    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(
        ["linaro_django_pagination.tests"],
        extra_tests=[doctest.DocTestSuite('linaro_django_pagination.tests.test_main')]
    )
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()

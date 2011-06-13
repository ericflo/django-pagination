#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='linaro-django-pagination',
    version=version,
    description="linaro-django-pagination",
    long_description=open("README").read(),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='pagination,django',
    author='Zygmunt Krynicki',
    author_email='zygmunt.krynicki@linaro.org',
    url='https://github.com/zyga/django-pagination',
    test_suite='linaro_django_pagination.test_project.tests.run_tests',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'django >= 1.2',
    ],
    tests_require=[
        'django-testproject >= 0.1',
    ],
    include_package_data=True,
    zip_safe=False,
)

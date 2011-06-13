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
    url='http://launchpad.net/linaro-django-pagination/',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

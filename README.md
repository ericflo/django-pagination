django-pagination-py3
====================

![Python Compatibility](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg) [![PyPi Version](https://img.shields.io/pypi/v/django-pagination-py3.svg)](https://pypi.python.org/pypi/django-pagination-py3)  ![CI badge](https://github.com/matagus/django-pagination-py3/actions/workflows/ci.yml/badge.svg) [![codecov](https://codecov.io/gh/matagus/django-pagination-py3/graph/badge.svg?token=a64SxEDQk0)](https://codecov.io/gh/matagus/django-pagination-py3) [![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

A port of [ericflo/django-pagination](https://github.com/ericflo/django-pagination) to Python 3. Updated to be compatible with Django 4.x and 5.0.

For versions compatible with Django 3.x and Python 2.7+ please install or download version `1.2.0` from [Releases](https://github.com/matagus/django-pagination-py3/releases) or
[Pypi](https://pypi.org/project/django-pagination-py3/).

Features
========

- Really easy to use at template level.
- It preserves all request's querystring parameters.
- Settings to customize behavior.
- Translated to fr, de, es, pt, pl and pt_BR.
- A fully working example project.


Installation
============

Install using `pip` command:

```bash
pip install django-pagination-py3
```

...or clone the repo and install it using `pip`:

```bash
git clone git://github.com/matagus/django-pagination-py3.git
cd django-pagination-py3
pip install -e .
```

Add `pagination` INSTALLED_APPS to your `settings.py`:

```python
INSTALLED_APPS = (
    # ...
    "pagination",
)
```

Add the middleware:

```python
   MIDDLEWARE_CLASSES = (
       # ...
       'pagination.middleware.PaginationMiddleware',
   )
```

Add this line at the top of your template to load the pagination tags:

```html
  {% load pagination_tags %}
```

Decide on a variable that you would like to paginate, and use the autopaginate tag on that variable before iterating
over it. This could take one of two forms (using the canonical `object_list` as an example variable):

```html
  {% autopaginate object_list %}
```

This assumes that you would like to have the default 20 results per page. If you would like to specify your own amount
of results per page, you can specify that like so:

```html
  {% autopaginate object_list 10 %}
```

Note that this replaces ``object_list`` with the list for the current page, so you can iterate over the `object_list`
like you normally would.


Now you want to display the current page and the available pages, so somewhere after having used autopaginate, use the
paginate inclusion tag:

```html
  {% paginate %}
```

This does not take any arguments, but does assume that you have already called autopaginate, so make sure to do so first.


That's it! You have now paginated `object_list` and given users of the site a way to navigate between the different
pages--all without touching your views.


Running Tests
-------------

`hatch run test:test` will run the tests in every Python + Django versions combination.

`hatch run test.py3.12-5.0:test`: will run them for python 3.12 and Django 5.0. Please see possible combinations using
`hatch env show` ("test" matrix).


License
=======

`django-pagination-py3` is released under an BSD License - see the `LICENSE` file for more information.


Acknowledgements
================

Develop & built using [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Posts I learned from:

- [Switching to Hatch](https://andrich.me/2023/08/switching-to-hatch/)
- [Automate Hatch Publish with GitHub Actions](https://blog.pecar.me/automate-hatch-publish)

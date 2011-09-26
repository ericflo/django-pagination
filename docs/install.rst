============
Installation
============

Installing via pip
-------------------------

If you have pip_ installed, you can simply run the following command
to install django-pagination:

    pip install django-pagination

Installing the latest development version of django-pagination
---------------------------------------------------------------

To install, first check out the latest version of the application from
subversion:

    git clone git@github.com:ericflo/django-pagination.git

Now, link the inner ``pagination`` project to your Python path:

    sudo ln -s `pwd`/pagination SITE_PACKAGES_DIR/pagination

If you don't know the location of your site packages directory, this hack might
do the trick for you:

    sudo ln -s `pwd`/pagination `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`/pagination
    
Now it's installed!  Please see usage.txt for information on how to use this
application in your projects.

Installing via setup.py
-----------------------

Included with this application is a file named ``setup.py``.  It's possible to
use this file to install this application to your system, by invoking the
following command:

    sudo python setup.py install

Once that's done, you should be able to begin using django-pagination at will.

.. _pip: http://pypi.python.org/pypi/pip
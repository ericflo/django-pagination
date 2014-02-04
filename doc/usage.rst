.. _usage:

Usage
*****

How to use linaro-django-pagination
===================================

``linaro-django-pagination`` allows for easy Digg-style pagination without modifying
your views.

There are really 5 steps to setting it up with your projects (not including 
installation, which is covered in INSTALL.txt in this same directory.)

1. List this application in the ``INSTALLED_APPS`` portion of your settings
   file.  Your settings file might look something like::
   
       INSTALLED_APPS = (
           # ...
           'pagination',
       )


2. Install the pagination middleware.  Your settings file might look something
   like::
   
       MIDDLEWARE_CLASSES = (
           # ...
           'pagination.middleware.PaginationMiddleware',
       )

3. If it's not already added in your setup, add the request context processor.
   Note that context processors are set by default implicitly, so to set them
   explicitly, you need to copy and paste this code into your under
   the value TEMPLATE_CONTEXT_PROCESSORS::
   
        ("django.core.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request")

4. Add this line at the top of your template to load the pagination tags:

       {% load pagination_tags %}


5. Decide on a variable that you would like to paginate, and use the
   autopaginate tag on that variable before iterating over it.  This could 
   take one of two forms (using the canonical ``object_list`` as an example
   variable):
   
       {% autopaginate object_list %}
       
   This assumes that you would like to have the default 20 results per page.
   If you would like to specify your own amount of results per page, you can
   specify that like so:
   
       {% autopaginate object_list 10 %}
   
   Note that this replaces ``object_list`` with the list for the current page, so
   you can iterate over the ``object_list`` like you normally would.
   

6. Now you want to display the current page and the available pages, so
   somewhere after having used autopaginate, use the paginate inclusion tag:
   
       {% paginate %}
   
   This does not take any arguments, but does assume that you have already
   called autopaginate, so make sure to do so first.


That's it!  You have now paginated ``object_list`` and given users of the site
a way to navigate between the different pages--all without touching your views.

Custom pagination templates
===========================

In order to override the default pagination template use the extended form of
the ``paginate`` tag::

    {% autopaginate posts pagesize %}
    {% paginate using "pagination/blog/post.html" %}

The default pagination template is contained in the
``pagination/pagination.html`` file inside the distribution.

A Note About Uploads
====================

It is important, when using linaro-django-pagination in conjunction with file
uploads, to be aware of when ``request.page`` is accessed.  As soon as
``request.page`` is accessed, ``request.upload_handlers`` is frozen and cannot
be altered in any way.  It's a good idea to access the ``page`` attribute on
the request object as late as possible in your views.


Optional Settings
=================

In linaro-django-pagination, there are no required settings.  There are,
however, a small set of optional settings useful for changing the default
behavior of the pagination tags.  Here's an overview:

``PAGINATION_DEFAULT_PAGINATION``
    The default amount of items to show on a page if no number is specified.
    Defaults to 20

``PAGINATION_DEFAULT_WINDOW``
    The number of items to the left and to the right of the current page to
    display (accounting for ellipses). Defaults to 4.

``PAGINATION_DEFAULT_MARGIN``
    FIXME: This needs to be documented.

``PAGINATION_DEFAULT_ORPHANS``
    The number of orphans allowed.  According to the Django documentation,
    orphans are defined as::
    
        The minimum number of items allowed on the last page, defaults to zero.

``PAGINATION_INVALID_PAGE_RAISES_404``
    Determines whether an invalid page raises an ``Http404`` or just sets the
    ``invalid_page`` context variable.  ``True`` does the former and ``False``
    does the latter. Defaults to False

``PAGINATION_DISPLAY_PAGE_LINKS``
    If set to ``False``, links for single pages will not be displayed. Defaults to True.

``PAGINATION_PREVIOUS_LINK_DECORATOR``
    An HTML prefix for the previous page link; the default value is ``&lsaquo;&lsaquo;``.

``PAGINATION_NEXT_LINK_DECORATOR``
    An HTML postfix for the next page link; the default value is ``&rsaquo;&rsaquo;``.

``PAGINATION_DISPLAY_DISABLED_PREVIOUS_LINK``
    If set to ``False``, the previous page link will not be displayed if there's 
    no previous page. Defaults to False.

``PAGINATION_DISPLAY_DISABLED_NEXT_LINK``
    If set to ``False``, the next page link will not be displayed if there's no 
    next page. Defaults to False.

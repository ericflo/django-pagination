django-pagination
=================

A set of utilities for creating robust pagination tools throughout a django application.

This modification includes paginate_by tag for multi choice objects per page.

Installation:
=================
In 'settings.py' add following lines (if they aren't already added):

```python
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.static",
)
```

In the MIDDLEWARE_CLASSES add ```'pagination.middleware.PaginationMiddleware'```

And in the INSTALLED_APPS add ```'pagination'```


Example:
=================
{% perpageselect 10 20 30 %} will show dropdown list with choices 10, 20 and 30 objects per page.
{% perpageanchors 10 20 30 %} will show anchors with choices 10, 20 and 30 objects per page.


Usage:
=================
```
{% load pagination_tags %}

    {% autopaginate object_list 10 %} <!--OR THIS {% perpageselect 10 20 30 %} -->
        {% for post in object_list %}
           bla-bla-bla
        {% endfor %}
    {% paginate %}
```

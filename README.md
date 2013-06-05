django-pagination
=================

A set of utilities for creating robust pagination tools throughout a django application.

This modification includes paginate_by tag for multi choice objects per page.

Example:
=================
{% perpageselect 10 20 30 %} will show dropdown list with choices 10, 20 and 30 objects per page.
{% perpageanchors 10 20 30 %} will show anchors with choices 10, 20 and 30 objects per page.

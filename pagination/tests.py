"""
>>> from django.core.paginator import Paginator
>>> from pagination.templatetags.pagination_tags import paginate

>>> p = Paginator(range(15), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, 5, 6, 7, 8]

>>> p = Paginator(range(17), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> p = Paginator(range(19), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, None, 7, 8, 9, 10]

>>> p = Paginator(range(21), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, None, 8, 9, 10, 11]
"""
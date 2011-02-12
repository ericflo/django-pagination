"""
>>> from django.core.paginator import Paginator
>>> from pagination.templatetags.pagination_tags import paginate
>>> from django.template import Template, Context

>>> p = Paginator(range(15), 2)
>>> pg = paginate({'paginator': p, 'page_obj': p.page(1)})
>>> pg['pages']
[1, 2, 3, 4, 5, 6, 7, 8]
>>> pg['records']['first']
1
>>> pg['records']['last']
2

>>> p = Paginator(range(15), 2)
>>> pg = paginate({'paginator': p, 'page_obj': p.page(8)})
>>> pg['pages']
[1, 2, 3, 4, 5, 6, 7, 8]
>>> pg['records']['first']
15
>>> pg['records']['last']
15

>>> p = Paginator(range(17), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, 5, 6, 7, 8, 9]


# on start
# moving the window from 1 ... to end
# window size = 2, margin = 2
# [1] 2 3 4 5 ... 15, 16
# 1 [2] 3 4 5 ... 15, 16
# 1 2 [3] 4 5 ... 15, 16
# 1 2 3 [4] 5 6 ... 15, 16
# 1 2 3 4 [5] 6 7 ... 15, 16
# 1 2 3 4 5 [6] 7 8 ... 15, 16
# 1 2 ... 5 6 [7] 8 9 ... 15, 16

# window = 2 -> show 5 pages
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)}, 2, '', 2)['pages']
[1, 2, 3, 4, 5, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(2)}, 2, '', 2)['pages']
[1, 2, 3, 4, 5, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(3)}, 2, '', 2)['pages']
[1, 2, 3, 4, 5, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(4)}, 2, '', 2)['pages']
[1, 2, 3, 4, 5, 6, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(5)}, 2, '', 2)['pages']
[1, 2, 3, 4, 5, 6, 7, None, 15, 16]

# in the middle
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(7)}, 2, '', 2)['pages']
[1, 2, None, 5, 6, 7, 8, 9, None, 15, 16]

# on end
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(16)}, 2, '', 2)['pages']
[1, 2, None, 12, 13, 14, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(13)}, 2, '', 2)['pages']
[1, 2, None, 11, 12, 13, 14, 15, 16]


>>> p = Paginator(range(0), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1]



# no margin
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(3)}, 2, '', 0)['pages']
[1, 2, 3, 4, 5, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(5)}, 2, '', 0)['pages']
[None, 3, 4, 5, 6, 7, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(16)}, 2, '', 0)['pages']
[None, 12, 13, 14, 15, 16]


# special
# zero window, zero margin
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)}, 0, '', 0)['pages']
[1, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(2)}, 0, '', 0)['pages']
[None, 2, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(3)}, 0, '', 0)['pages']
[None, 3, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(10)}, 0, '', 0)['pages']
[None, 10, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(14)}, 0, '', 0)['pages']
[None, 14, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(15)}, 0, '', 0)['pages']
[None, 15, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(16)}, 0, '', 0)['pages']
[None, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(5)}, 0, '', 1)['pages']
[1, None, 5, None, 16]




"""

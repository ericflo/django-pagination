"""
>>> from django.core.paginator import Paginator
>>> from pagination.templatetags.pagination_tags import paginate
>>> from django.template import Template, Context

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

# Testing orphans
>>> p = Paginator(range(5), 2, 1)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2]

>>> p = Paginator(range(21), 2, 1)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1, 2, 3, 4, None, 7, 8, 9, 10]

>>> t = Template("{% load pagination_tags %}{% autopaginate var 2 %}{% paginate %}")

# WARNING: Please, please nobody read this portion of the code!
>>> class GetProxy(object):
...     def __iter__(self): yield self.__dict__.__iter__
...     def copy(self): return self
...     def urlencode(self): return u''
...     def keys(self): return []
>>> class RequestProxy(object):
...     page = 1
...     GET = GetProxy()
>>>
# ENDWARNING

>>> t.render(Context({'var': range(21), 'request': RequestProxy()}))
u'\\n\\n<div class="pagination">...
>>>
>>> t = Template("{% load pagination_tags %}{% autopaginate var %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'request': RequestProxy()}))
u'\\n\\n<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var 20 %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'request': RequestProxy()}))
u'\\n\\n<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var by %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'by': 20, 'request': RequestProxy()}))
u'\\n\\n<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var by as foo %}{{ foo }}")
>>> t.render(Context({'var': range(21), 'by': 20, 'request': RequestProxy()}))
u'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]'
>>>

# Testing InfinitePaginator

>>> from paginator import InfinitePaginator

>>> InfinitePaginator
<class 'pagination.paginator.InfinitePaginator'>
>>> p = InfinitePaginator(range(20), 2, link_template='/bacon/page/%d')
>>> p.validate_number(2)
2
>>> p.orphans
0
>>> p3 = p.page(3)
>>> p3
<Page 3>
>>> p3.end_index()
6
>>> p3.has_next()
True
>>> p3.has_previous()
True
>>> p.page(10).has_next()
False
>>> p.page(1).has_previous()
False
>>> p3.next_link()
'/bacon/page/4'
>>> p3.previous_link()
'/bacon/page/2'

# Testing FinitePaginator

>>> from paginator import FinitePaginator

>>> FinitePaginator
<class 'pagination.paginator.FinitePaginator'>
>>> p = FinitePaginator(range(20), 2, offset=10, link_template='/bacon/page/%d')
>>> p.validate_number(2)
2
>>> p.orphans
0
>>> p3 = p.page(3)
>>> p3
<Page 3>
>>> p3.start_index()
10
>>> p3.end_index()
6
>>> p3.has_next()
True
>>> p3.has_previous()
True
>>> p3.next_link()
'/bacon/page/4'
>>> p3.previous_link()
'/bacon/page/2'

>>> p = FinitePaginator(range(20), 20, offset=10, link_template='/bacon/page/%d')
>>> p2 = p.page(2)
>>> p2
<Page 2>
>>> p2.has_next()
False
>>> p3.has_previous()
True
>>> p2.next_link()

>>> p2.previous_link()
'/bacon/page/1'

"""
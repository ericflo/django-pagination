# Copyright (c) 2008, Eric Florenzano
# Copyright (c) 2010, 2011 Linaro Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of the author nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""
>>> from django.core.paginator import Paginator
>>> from linaro_django_pagination.templatetags.pagination_tags import paginate
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
>>> paginate({'paginator': p, 'page_obj': p.page(1)}, 2, 2)['pages']
[1, 2, 3, 4, 5, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(2)}, 2, 2)['pages']
[1, 2, 3, 4, 5, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(3)}, 2, 2)['pages']
[1, 2, 3, 4, 5, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(4)}, 2, 2)['pages']
[1, 2, 3, 4, 5, 6, None, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(5)}, 2, 2)['pages']
[1, 2, 3, 4, 5, 6, 7, None, 15, 16]

# in the middle
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(7)}, 2, 2)['pages']
[1, 2, None, 5, 6, 7, 8, 9, None, 15, 16]

# on end
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(16)}, 2, 2)['pages']
[1, 2, None, 12, 13, 14, 15, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(13)}, 2, 2)['pages']
[1, 2, None, 11, 12, 13, 14, 15, 16]


>>> p = Paginator(range(0), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)})['pages']
[1]



# no margin
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(3)}, 2, 0)['pages']
[1, 2, 3, 4, 5, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(5)}, 2, 0)['pages']
[None, 3, 4, 5, 6, 7, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(16)}, 2, 0)['pages']
[None, 12, 13, 14, 15, 16]


# special
# zero window, zero margin
>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(1)}, 0, 0)['pages']
[1, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(2)}, 0, 0)['pages']
[None, 2, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(3)}, 0, 0)['pages']
[None, 3, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(10)}, 0, 0)['pages']
[None, 10, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(14)}, 0, 0)['pages']
[None, 14, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(15)}, 0, 0)['pages']
[None, 15, None]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(16)}, 0, 0)['pages']
[None, 16]

>>> p = Paginator(range(31), 2)
>>> paginate({'paginator': p, 'page_obj': p.page(5)}, 0, 1)['pages']
[1, None, 5, None, 16]

>>> p = Paginator(range(21), 2, 1)
>>> paginate({'paginator': p, 'page_obj': p.page(1)}, 0, 4)['pages']
[1, 2, 3, 4, None, 7, 8, 9, 10]

# Testing template rendering

>>> t = Template("{% load pagination_tags %}{% autopaginate var 2 %}{% paginate %}")

>>> from django.http import HttpRequest as DjangoHttpRequest
>>> class HttpRequest(DjangoHttpRequest):
...     page = lambda self, suffix: 1

>>> t.render(Context({'var': range(21), 'request': HttpRequest()}))
u'\\n...\\n...<div class="pagination">...
>>>
>>> t = Template("{% load pagination_tags %}{% autopaginate var %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'request': HttpRequest()}))
u'\\n...\\n...<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var 20 %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'request': HttpRequest()}))
u'\\n...\\n...<div class="pagination">...
>>> t = Template("{% load pagination_tags %}{% autopaginate var by %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()}))
u'\\n...\\n...<div class="pagination">...<a href="?page=2"...
>>> t = Template("{% load pagination_tags %}{% autopaginate var by as foo %}{{ foo }}")
>>> t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()}))
u'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]'
>>>
>>> t = Template("{% load pagination_tags %}{% autopaginate var2 by as foo2 %}{% paginate %}{% autopaginate var by as foo %}{% paginate %}")
>>> t.render(Context({'var': range(21), 'var2': range(50, 121), 'by': 20, 'request': HttpRequest()}))
u'\\n...\\n...<div class="pagination">...<a href="?page_var2=2"...<a href="?page_var=2"...
>>>

# Testing InfinitePaginator

>>> from paginator import InfinitePaginator

>>> InfinitePaginator
<class 'linaro_django_pagination.paginator.InfinitePaginator'>
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
<class 'linaro_django_pagination.paginator.FinitePaginator'>
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

>>> from linaro_django_pagination.middleware import PaginationMiddleware
>>> from django.core.handlers.wsgi import WSGIRequest
>>> from StringIO import StringIO
>>> middleware = PaginationMiddleware()
>>> request = WSGIRequest({'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': 'multipart', 'wsgi.input': StringIO()})
>>> middleware.process_request(request)
>>> request.upload_handlers.append('asdf')
"""

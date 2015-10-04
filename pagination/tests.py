from StringIO import StringIO

from django.core.paginator import Paginator
from django.core.handlers.wsgi import WSGIRequest
from django.template import Template, Context
from django.http import HttpRequest as DjangoHttpRequest

from django.test import SimpleTestCase

from pagination.templatetags.pagination_tags import paginate
from pagination.paginator import FinitePaginator, InfinitePaginator
from pagination.middleware import PaginationMiddleware


class HttpRequest(DjangoHttpRequest):
    page = lambda self, suffix: 1


class PaginationTestCase(SimpleTestCase):
    def test_paginator_1(self):
        p = Paginator(range(15), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(pg['records']['first'], 1)
        self.assertEqual(pg['records']['last'], 2)

    def test_paginator_2(self):
        p = Paginator(range(15), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(8)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(pg['records']['first'], 15)
        self.assertEqual(pg['records']['last'], 15)

    def test_paginator_3(self):
        p = Paginator(range(17), 2)
        self.assertEqual(
            paginate({'paginator': p, 'page_obj': p.page(1)})['pages'],
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        )

    def test_paginator_4(self):
        p = Paginator(range(19), 2)
        self.assertEqual(
            paginate({'paginator': p, 'page_obj': p.page(1)})['pages'],
            [1, 2, 3, 4, None, 7, 8, 9, 10]
        )

    def test_paginator_5(self):
        p = Paginator(range(21), 2)
        self.assertEqual(
            paginate({'paginator': p, 'page_obj': p.page(1)})['pages'],
            [1, 2, 3, 4, None, 8, 9, 10, 11]
        )

    def test_paginator_6(self):
        p = Paginator(range(5), 2, 1)
        self.assertEqual(
            paginate({'paginator': p, 'page_obj': p.page(1)})['pages'],
            [1, 2]
        )

    def test_paginator_7(self):
        p = Paginator(range(21), 2, 1)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, None, 7, 8, 9, 10])
        self.assertEqual(pg['records']['first'], 1)
        self.assertEqual(pg['records']['last'], 2)

    def test_paginator_8(self):
        p = Paginator(range(21), 2, 1)
        pg = paginate({'paginator': p, 'page_obj': p.page(10)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(pg['records']['first'], 19)
        self.assertEqual(pg['records']['last'], 21)

    def test_paginator_9(self):
        p = Paginator(range(21), 2, 1)
        self.assertEqual(
            paginate({'paginator': p, 'page_obj': p.page(1)})['pages'],
            [1, 2, 3, 4, None, 7, 8, 9, 10]
        )

    def test_template_1(self):
        t = Template("{% load pagination_tags %}{% autopaginate var 2 %}{% paginate %}")

        self.assertIn(
            u'<div class="pagination">',
            t.render(Context({'var': range(21), 'request': HttpRequest()}))
        )

    def test_template_2(self):
        t = Template("{% load pagination_tags %}{% autopaginate var %}{% paginate %}")
        self.assertIn(
            u'<div class="pagination">',
            t.render(Context({'var': range(21), 'request': HttpRequest()}))
        )

    def test_template_3(self):
        t = Template("{% load pagination_tags %}{% autopaginate var 20 %}{% paginate %}")
        self.assertIn(
            u'<div class="pagination">',
            t.render(Context({'var': range(21), 'request': HttpRequest()}))
        )

    def test_template_4(self):
        t = Template("{% load pagination_tags %}{% autopaginate var by %}{% paginate %}")
        r = t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()}))

        self.assertIn(u'<div class="pagination">', r)
        self.assertIn(u'<a href="?page=2"', r)

    def test_template_5(self):
        t = Template("{% load pagination_tags %}{% autopaginate var by as foo %}{{ foo }}")
        self.assertEqual(
            t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()})),
            u'[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]'
        )

    def test_template_6(self):
        t = Template("{% load pagination_tags %}{% autopaginate var2 by as foo2 %}{% paginate %}{% autopaginate var by as foo %}{% paginate %}")
        r = t.render(Context({'var': range(21), 'var2': range(50, 121), 'by': 20, 'request': HttpRequest()}))
        self.assertIn(u'<div class="pagination">', r)
        self.assertIn(u'<a href="?page_var2=2"', r)
        self.assertIn(u'<a href="?page_var=2"', r)

    def test_infinite_paginator(self):
        p = InfinitePaginator(range(20), 2, link_template='/bacon/page/%d')
        self.assertEqual(p.validate_number(2), 2)
        self.assertEqual(p.orphans, 0)

        p3 = p.page(3)
        self.assertEqual(repr(p3), u'<Page 3>')
        self.assertEqual(p3.end_index(), 6)

        self.assertTrue(p3.has_next())
        self.assertTrue(p3.has_previous())

        self.assertEqual(p3.next_link(), '/bacon/page/4')
        self.assertEqual(p3.previous_link(), '/bacon/page/2')

        self.assertFalse(p.page(10).has_next())
        self.assertFalse(p.page(1).has_previous())

    def test_finite_paginator_1(self):
        p = FinitePaginator(range(20), 2, offset=10, link_template='/bacon/page/%d')
        self.assertEqual(p.validate_number(2), 2)
        self.assertEqual(p.orphans, 0)

        p3 = p.page(3)
        self.assertEqual(repr(p3), u'<Page 3>')
        self.assertEqual(p3.start_index(), 10)
        self.assertEqual(p3.end_index(), 6)

        self.assertTrue(p3.has_next())
        self.assertTrue(p3.has_previous())

        self.assertEqual(p3.next_link(), '/bacon/page/4')
        self.assertEqual(p3.previous_link(), '/bacon/page/2')

    def test_finite_paginator_2(self):
        p = FinitePaginator(range(20), 20, offset=10, link_template='/bacon/page/%d')

        p2 = p.page(2)
        self.assertEqual(repr(p2), u'<Page 2>')

        self.assertFalse(p2.has_next())
        self.assertTrue(p2.has_previous())

        self.assertEqual(p2.next_link(), None)
        self.assertEqual(p2.previous_link(), '/bacon/page/1')

    def test_middleware(self):
        middleware = PaginationMiddleware()
        request = WSGIRequest({'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': 'multipart', 'wsgi.input': StringIO()})
        middleware.process_request(request)
        request.upload_handlers.append('asdf')

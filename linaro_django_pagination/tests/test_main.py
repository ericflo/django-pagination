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

from django.core.paginator import Paginator
from django.http import HttpRequest as DjangoHttpRequest
from django.template import Template, Context

try:
    from django.test import SimpleTestCase
except ImportError:  # Django 1.2 compatible
    from django.test import TestCase as SimpleTestCase

from linaro_django_pagination.paginator import InfinitePaginator, FinitePaginator
from linaro_django_pagination.templatetags.pagination_tags import paginate
from linaro_django_pagination.middleware import PaginationMiddleware


class HttpRequest(DjangoHttpRequest):
     page = lambda self, suffix: 1


class CommonTestCase(SimpleTestCase):
    def test_records_for_the_first_page(self):
        p = Paginator(range(15), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertListEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(pg['records']['first'], 1)
        self.assertEqual(pg['records']['last'], 2)

    def test_records_for_the_last_page(self):
        p = Paginator(range(15), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(8)})
        self.assertListEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(pg['records']['first'], 15)
        self.assertEqual(pg['records']['last'], 15)

    def test_pages_list(self):
        p = Paginator(range(17), 2)
        self.assertEqual(paginate({'paginator': p, 'page_obj': p.page(1)})['pages'], [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_page_with_empty_objects_list(self):
        p = Paginator(range(0), 2)
        self.assertListEqual(paginate({'paginator': p, 'page_obj': p.page(1)})['pages'], [1])


class DefaultWindowTestCase(SimpleTestCase):
    """
    Test paginate using default window setting
    moving the window from 1 ... to end
    window size = 2, margin = 2
    window = 2 -> show 5 pages
    """
    def setUp(self):
        self.p = Paginator(range(31), 2)

    def test_on_start_page_1(self):
        # [1] 2 3 4 5 ... 15, 16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(1)}, 2, 2)['pages'],
            [1, 2, 3, 4, 5, None, 15, 16]
        )

    def test_on_start_page_2(self):
        # 1 [2] 3 4 5 ... 15, 16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(2)}, 2, 2)['pages'],
            [1, 2, 3, 4, 5, None, 15, 16]
        )

    def test_on_start_page_3(self):
        # 1 2 [3] 4 5 ... 15, 16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(3)}, 2, 2)['pages'],
            [1, 2, 3, 4, 5, None, 15, 16]
        )

    def test_on_start_page_4(self):
        # 1 2 3 [4] 5 6 ... 15, 16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(4)}, 2, 2)['pages'],
            [1, 2, 3, 4, 5, 6, None, 15, 16])

    def test_on_start_page_5(self):
        # 1 2 3 4 [5] 6 7 ... 15, 16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(5)}, 2, 2)['pages'],
            [1, 2, 3, 4, 5, 6, 7, None, 15, 16]
        )

    def test_in_middle(self):
        # 1 2 ... 5 6 [7] 8 9 ... 15, 16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(7)}, 2, 2)['pages'],
            [1, 2, None, 5, 6, 7, 8, 9, None, 15, 16]
        )

    def test_on_end_page_13(self):
        # 1 2 ... 12 [13] 14 15 16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(13)}, 2, 2)['pages'],
            [1, 2, None, 11, 12, 13, 14, 15, 16],
        )

    def test_on_end(self):
        # 1 2 ... 12 13 14 15 [16
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(16)}, 2, 2)['pages'],
            [1, 2, None, 12, 13, 14, 15, 16]
        )


class NoMarginTestCase(SimpleTestCase):
    def setUp(self):
        self.p = Paginator(range(31), 2)

    def test_on_start(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(3)}, 2, 0)['pages'],
            [1, 2, 3, 4, 5, None],
        )

    def test_in_middle(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(5)}, 2, 0)['pages'],
            [None, 3, 4, 5, 6, 7, None],
        )

    def test_on_end(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(16)}, 2, 0)['pages'],
            [None, 12, 13, 14, 15, 16],
        )


class ZeroWindowZeroMarginTestCase(SimpleTestCase):
    """
    Test paginate using window=0 and margin=0
    """
    def setUp(self):
        self.p = Paginator(range(31), 2)

    def test_on_start_page_1(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(1)}, 0, 0)['pages'],
            [1, None],
        )

    def test_in_middle_page_2(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(2)}, 0, 0)['pages'],
            [None, 2, None],
        )

    def test_in_middle_page_3(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(3)}, 0, 0)['pages'],
            [None, 3, None],
        )

    def test_in_middle_page_10(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(10)}, 0, 0)['pages'],
            [None, 10, None],
        )

    def test_in_middle_page_14(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(14)}, 0, 0)['pages'],
            [None, 14, None],
        )

    def test_in_middle_page_15(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(15)}, 0, 0)['pages'],
            [None, 15, None],
        )

    def test_on_end_page_16(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(16)}, 0, 0)['pages'],
            [None, 16],
        )


class NoEllipsisTestCase(SimpleTestCase):
    """
    Tests a case where should be no any ellipsis pages.
    """
    def setUp(self):
        self.p = Paginator(range(100), 25)

    def test_on_start(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(1)}, 2, 0)['pages'],
            [1, 2, 3, 4],
        )

    def test_in_middle_page_2(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(2)}, 2, 0)['pages'],
            [1, 2, 3, 4],
        )

    def test_in_middle_page_3(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(3)}, 2, 0)['pages'],
            [1, 2, 3, 4],
        )

    def test_on_end(self):
        self.assertListEqual(
            paginate({'paginator': self.p, 'page_obj': self.p.page(4)}, 2, 0)['pages'],
            [1, 2, 3, 4],
        )


class SpecialTestCase(SimpleTestCase):
    def test_middle_with_no_window_and_margin_1(self):
        p = Paginator(range(31), 2)
        self.assertListEqual(
            paginate({'paginator': p, 'page_obj': p.page(5)}, 0, 1)['pages'],
            [1, None, 5, None, 16],
        )

    def test_middle_with_no_window_and_margin_4(self):
        p = Paginator(range(21), 2, 1)
        self.assertListEqual(
            paginate({'paginator': p, 'page_obj': p.page(1)}, 0, 4)['pages'],
            [1, 2, 3, 4, None, 7, 8, 9, 10],
        )


class TemplateRenderingTestCase(SimpleTestCase):
    def test_default_tag_options(self):
        t = Template("{% load pagination_tags %}{% autopaginate var %}{% paginate %}")
        self.assertIn(
            '<div class="pagination">',
            t.render(Context({'var': range(21), 'request': HttpRequest()})),
        )

    def test_paginate_by_option(self):
        t = Template("{% load pagination_tags %}{% autopaginate var 20 %}{% paginate %}")
        self.assertIn(
            '<div class="pagination">',
            t.render(Context({'var': range(21), 'request': HttpRequest()})),
        )

    def test_orphans_option(self):
        t = Template("{% load pagination_tags %}{% autopaginate var by %}{% paginate %}")
        content = t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()}))
        self.assertIn('<div class="pagination">', content)
        self.assertIn('<a href="?page=2"', content)

    def test_as_option(self):
        t = Template("{% load pagination_tags %}{% autopaginate var by as foo %}{{ foo }}")
        self.assertEqual(
            t.render(Context({'var': range(21), 'by': 20, 'request': HttpRequest()})),
            str(range(20)),
        )

    def test_multiple_pagination(self):
        t = Template("{% load pagination_tags %}{% autopaginate var2 by as foo2 %}{% paginate %}"
                     "{% autopaginate var by as foo %}{% paginate %}")
        content = t.render(Context({'var': range(21), 'var2': range(50, 121), 'by': 20, 'request': HttpRequest()}))
        self.assertIn('<div class="pagination">', content)
        self.assertIn('<a href="?page_var2=2"', content)
        self.assertIn('<a href="?page_var=2"', content)


class InfinitePaginatorTestCase(SimpleTestCase):
    def setUp(self):
        self.p = InfinitePaginator(range(20), 2, link_template='/bacon/page/%d')

    def test_paginator_repr(self):
        self.assertEqual(
            repr(InfinitePaginator),
            "<class 'linaro_django_pagination.paginator.InfinitePaginator'>",
        )

    def test_validate_number(self):
        self.assertEqual(self.p.validate_number(2), 2)

    def test_orphans(self):
        self.assertEqual(self.p.orphans, 0)

    def test_page_repr(self):
        self.assertEqual(repr(self.p.page(3)), '<Page 3>')

    def test_page_end_index(self):
        self.assertEqual(self.p.page(3).end_index(), 6)

    def test_page_has_next(self):
        self.assertTrue(self.p.page(3).has_next(), True)

    def test_page_has_previous(self):
        self.assertTrue(self.p.page(3).has_previous(), True)

    def test_page_next_link(self):
        self.assertEqual(self.p.page(3).next_link(), '/bacon/page/4')

    def test_page_previous_link(self):
        self.assertEqual(self.p.page(3).previous_link(), '/bacon/page/2')

    def test_last_page_which_has_no_next_page(self):
        self.assertFalse(self.p.page(10).has_next())

    def test_first_page_which_has_no_previous_page(self):
        self.assertFalse(self.p.page(1).has_previous())


class FinitePaginatorTestCase(SimpleTestCase):
    def setUp(self):
        self.p = FinitePaginator(range(20), 2, offset=10, link_template='/bacon/page/%d')

    def test_repr(self):
        self.assertEqual(
            repr(FinitePaginator),
            "<class 'linaro_django_pagination.paginator.FinitePaginator'>"
        )

    def test_validate_number(self):
        self.assertEqual(self.p.validate_number(2), 2)

    def test_orphans(self):
        self.assertEqual(self.p.orphans, 0)

    def test_page_repr(self):
        self.assertEqual(repr(self.p.page(3)), '<Page 3>')

    def test_page_start_index(self):
        self.assertEqual(self.p.page(3).start_index(), 10)

    def test_page_end(self):
        self.assertEqual(self.p.page(3).end_index(), 6)

    def test_page_has_next(self):
        self.assertTrue(self.p.page(3).has_next(), True)

    def test_page_has_previous(self):
        self.assertTrue(self.p.page(3).has_previous(), True)

    def test_page_next_link(self):
        self.assertEqual(self.p.page(3).next_link(), '/bacon/page/4')

    def test_page_previous_link(self):
        self.assertEqual(self.p.page(3).previous_link(), '/bacon/page/2')

    def test_on_start_page_repr(self):
        self.assertEqual(repr(self.p.page(2)), '<Page 2>')

    def test_on_start_has_no_next(self):
        self.assertTrue(self.p.page(2).has_next(), False)

    def test_on_start_has_previous(self):
        self.assertTrue(self.p.page(2).has_previous(), True)

    def test_on_start_has_next_link(self):
        self.assertEqual(self.p.page(2).next_link(), '/bacon/page/3')

    def test_on_start_has_previous_link(self):
        self.assertEqual(self.p.page(2).previous_link(), '/bacon/page/1')


class MiddlewareTestCase(SimpleTestCase):
    """
    Test middleware
    """
    def test_get_page_in_request(self):
        middleware = PaginationMiddleware()
        request = DjangoHttpRequest()
        middleware.process_request(request)
        self.assertEqual(request.page(''), 1)

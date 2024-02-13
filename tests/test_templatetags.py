from django.core.paginator import Paginator
from django.test import TestCase
from django.http import HttpRequest as DjangoHttpRequest
from django.template import Context, Template

from pagination.templatetags.pagination_tags import paginate


class PaginateTestCase(TestCase):
    def test_first_page_pagination(self):
        p = Paginator(range(15), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(pg['records']['first'], 1)
        self.assertEqual(pg['records']['last'], 2)

    def test_last_page_pagination(self):
        p = Paginator(range(15), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(8)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(pg['records']['first'], 15)
        self.assertEqual(pg['records']['last'], 15)

    def test_pages(self):
        p = Paginator(range(17), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(pg["pages"], [1, 2, 3, 4, 5, 6, 7, 8, 9])

        p = Paginator(range(19), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(pg["pages"], [1, 2, 3, 4, None, 7, 8, 9, 10])

        p = Paginator(range(21), 2)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(pg["pages"], [1, 2, 3, 4, None, 8, 9, 10, 11])


class OrphansTestCase(TestCase):
    def test_pagination_first_page(self):
        p = Paginator(range(5), 2, 1)
        result = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(result['pages'], [1, 2])

    def test_pagination_middle_page(self):
        p = Paginator(range(21), 2, 1)
        pg = paginate({'paginator': p, 'page_obj': p.page(1)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, None, 7, 8, 9, 10])
        self.assertEqual(pg['records']['first'], 1)
        self.assertEqual(pg['records']['last'], 2)

    def test_pagination_last_page(self):
        p = Paginator(range(21), 2, 1)
        pg = paginate({'paginator': p, 'page_obj': p.page(10)})
        self.assertEqual(pg['pages'], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(pg['records']['first'], 19)
        self.assertEqual(pg['records']['last'], 21)


class HttpRequest(DjangoHttpRequest):
    page = 1


class AutopaginateTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.item_list = list(range(21))

    def test_autopaginate_default(self):
        t = Template("{% load pagination_tags %}{% autopaginate var %}{% paginate %}")
        rendered = t.render(Context({'var': self.item_list, 'request': self.request}))
        # You might need to adjust the assertion depending on the actual output
        self.assertIn('<div class="pagination">', rendered)

    def test_autopaginate_custom(self):
        t = Template("{% load pagination_tags %}{% autopaginate var 20 %}{% paginate %}")
        rendered = t.render(Context({'var': self.item_list, 'request': self.request}))
        # You might need to adjust the assertion depending on the actual output
        self.assertIn('<div class="pagination">', rendered)

    def test_autopaginate_variable(self):
        t = Template("{% load pagination_tags %}{% autopaginate var by %}{% paginate %}")
        rendered = t.render(Context({'var': self.item_list, 'by': 20, 'request': self.request}))
        # You might need to adjust the assertion depending on the actual output
        self.assertIn('<div class="pagination">', rendered)

    def test_autopaginate_as_variable(self):
        t = Template("{% load pagination_tags %}{% autopaginate var by as foo %}{{ foo }}")
        rendered = t.render(Context({'var': self.item_list, 'by': 20, 'request': self.request}))
        self.assertEqual(rendered, '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]')

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


from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.template import (
    Context,
    Library,
    Node,
    TemplateSyntaxError,
    Variable,
    loader,
)

try:
    from django.template.base import TOKEN_BLOCK
except ImportError:     # Django < 1.8
    from django.template import TOKEN_BLOCK

from django.template.loader import select_template
from django.utils.text import unescape_string_literal

# TODO, import this normally later on
from linaro_django_pagination.settings import *


def do_autopaginate(parser, token):
    """
    Splits the arguments to the autopaginate tag and formats them correctly.

    Syntax is:

        autopaginate QUERYSET [PAGINATE_BY] [ORPHANS] [as NAME]
    """
    # Check whether there are any other autopaginations are later in this template
    expr = lambda obj: (obj.token_type == TOKEN_BLOCK and \
        len(obj.split_contents()) > 0 and obj.split_contents()[0] == "autopaginate")
    multiple_paginations = len([tok for tok in parser.tokens if expr(tok)]) > 0

    i = iter(token.split_contents())
    paginate_by = None
    queryset_var = None
    context_var = None
    orphans = None
    word = None
    try:
        word = next(i)
        assert word == "autopaginate"
        queryset_var = next(i)
        word = next(i)
        if word != "as":
            paginate_by = word
            try:
                paginate_by = int(paginate_by)
            except ValueError:
                pass
            word = next(i)
        if word != "as":
            orphans = word
            try:
                orphans = int(orphans)
            except ValueError:
                pass
            word = next(i)
        assert word == "as"
        context_var = next(i)
    except StopIteration:
        pass
    if queryset_var is None:
        raise TemplateSyntaxError(
            "Invalid syntax. Proper usage of this tag is: "
            "{% autopaginate QUERYSET [PAGINATE_BY] [ORPHANS]"
            " [as CONTEXT_VAR_NAME] %}")
    return AutoPaginateNode(queryset_var, multiple_paginations, paginate_by, orphans, context_var)


class AutoPaginateNode(Node):
    """
    Emits the required objects to allow for Digg-style pagination.

    First, it looks in the current context for the variable specified, and using
    that object, it emits a simple ``Paginator`` and the current page object
    into the context names ``paginator`` and ``page_obj``, respectively.

    It will then replace the variable specified with only the objects for the
    current page.

    .. note::

        It is recommended to use *{% paginate %}* after using the autopaginate
        tag.  If you choose not to use *{% paginate %}*, make sure to display the
        list of available pages, or else the application may seem to be buggy.
    """
    def __init__(self, queryset_var,  multiple_paginations, paginate_by=None,
                 orphans=None, context_var=None):
        if paginate_by is None:
            paginate_by = DEFAULT_PAGINATION
        if orphans is None:
            orphans = DEFAULT_ORPHANS
        self.queryset_var = Variable(queryset_var)
        if isinstance(paginate_by, int):
            self.paginate_by = paginate_by
        else:
            self.paginate_by = Variable(paginate_by)
        if isinstance(orphans, int):
            self.orphans = orphans
        else:
            self.orphans = Variable(orphans)
        self.context_var = context_var
        self.multiple_paginations = multiple_paginations

    def render(self, context):
        if self.multiple_paginations or getattr(context, "paginator", None):
            page_suffix = '_%s' % self.queryset_var
        else:
            page_suffix = ''

        key = self.queryset_var.var
        value = self.queryset_var.resolve(context)
        if isinstance(self.paginate_by, int):
            paginate_by = self.paginate_by
        else:
            paginate_by = self.paginate_by.resolve(context)
        if isinstance(self.orphans, int):
            orphans = self.orphans
        else:
            orphans = self.orphans.resolve(context)
        paginator = Paginator(value, paginate_by, orphans)
        try:
            request = context['request']
        except KeyError:
            raise ImproperlyConfigured(
                "You need to enable 'django.core.context_processors.request'."
                " See linaro-django-pagination/README file for TEMPLATE_CONTEXT_PROCESSORS details")
        try:
            page_obj = paginator.page(request.page(page_suffix))
        except InvalidPage:
            if INVALID_PAGE_RAISES_404:
                raise Http404('Invalid page requested.  If DEBUG were set to ' +
                    'False, an HTTP 404 page would have been shown instead.')
            context[key] = []
            context['invalid_page'] = True
            return u''
        if self.context_var is not None:
            context[self.context_var] = page_obj.object_list
        else:
            context[key] = page_obj.object_list
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['page_suffix'] = page_suffix
        return u''


class PaginateNode(Node):

    def __init__(self, template=None):
        self.template = template

    def render(self, context):
        template_list = ['pagination/pagination.html']
        new_context = paginate(context)
        if self.template:
            template_list.insert(0, self.template)
        return loader.render_to_string(template_list, new_context,
            context_instance = context)



def do_paginate(parser, token):
    """
    Emits the pagination control for the most recent autopaginate list

    Syntax is:

        paginate [using "TEMPLATE"]

    Where TEMPLATE is a quoted template name. If missing the default template
    is used (paginate/pagination.html).
    """
    argv = token.split_contents()
    argc = len(argv)
    if argc == 1:
        template = None
    elif argc == 3 and argv[1] == 'using':
        template = unescape_string_literal(argv[2])
    else:
        raise TemplateSyntaxError(
            "Invalid syntax. Proper usage of this tag is: "
            "{% paginate [using \"TEMPLATE\"] %}")
    return PaginateNode(template)


def paginate(context, window=DEFAULT_WINDOW, margin=DEFAULT_MARGIN):
    """
    Renders the ``pagination/pagination.html`` template, resulting in a
    Digg-like display of the available pages, given the current page.  If there
    are too many pages to be displayed before and after the current page, then
    elipses will be used to indicate the undisplayed gap between page numbers.

    Requires one argument, ``context``, which should be a dictionary-like data
    structure and must contain the following keys:

    ``paginator``
        A ``Paginator`` or ``QuerySetPaginator`` object.

    ``page_obj``
        This should be the result of calling the page method on the
        aforementioned ``Paginator`` or ``QuerySetPaginator`` object, given
        the current page.

    This same ``context`` dictionary-like data structure may also include:

    ``getvars``
        A dictionary of all of the **GET** parameters in the current request.
        This is useful to maintain certain types of state, even when requesting
        a different page.

    Argument ``window`` is number to pages before/after current page. If window
    exceeds pagination border (1 and end), window is moved to left or right.

    Argument ``margin``` is number of pages on start/end of pagination.
    Example:
        window=2, margin=1, current=6     1 ... 4 5 [6] 7 8 ... 11
        window=2, margin=0, current=1     [1] 2 3 4 5 ...
        window=2, margin=0, current=5     ... 3 4 [5] 6 7 ...
        window=2, margin=0, current=11     ... 7 8 9 10 [11]
        """

    if window < 0:
        raise ValueError('Parameter "window" cannot be less than zero')
    if margin < 0:
        raise ValueError('Parameter "margin" cannot be less than zero')
    try:
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_suffix = context.get('page_suffix', '')
        page_range = paginator.page_range
        # Calculate the record range in the current page for display.
        records = {'first': 1 + (page_obj.number - 1) * paginator.per_page}
        records['last'] = records['first'] + paginator.per_page - 1
        if records['last'] + paginator.orphans >= paginator.count:
            records['last'] = paginator.count

        # figure window
        window_start = page_obj.number - window - 1
        window_end = page_obj.number + window

        # solve if window exceeded page range
        if window_start < 0:
            window_end = window_end - window_start
            window_start = 0
        if window_end > paginator.num_pages:
            window_start = window_start - (window_end - paginator.num_pages)
            window_end = paginator.num_pages
        pages = page_range[window_start:window_end]

        # figure margin and add elipses
        if margin > 0:
            # figure margin
            tmp_pages = set(pages)
            tmp_pages = tmp_pages.union(page_range[:margin])
            tmp_pages = tmp_pages.union(page_range[-margin:])
            tmp_pages = list(tmp_pages)
            tmp_pages.sort()
            pages = []
            pages.append(tmp_pages[0])
            for i in range(1, len(tmp_pages)):
                # figure gap size => add elipses or fill in gap
                gap = tmp_pages[i] - tmp_pages[i - 1]
                if gap >= 3:
                    pages.append(None)
                elif gap == 2:
                    pages.append(tmp_pages[i] - 1)
                pages.append(tmp_pages[i])
        else:
            if pages[0] != 1:
                pages.insert(0, None)
            if pages[-1] != paginator.num_pages:
                pages.append(None)

        new_context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': getattr(settings, "STATIC_URL", None),
            'disable_link_for_first_page': DISABLE_LINK_FOR_FIRST_PAGE,
            'display_disabled_next_link': DISPLAY_DISABLED_NEXT_LINK,
            'display_disabled_previous_link': DISPLAY_DISABLED_PREVIOUS_LINK,
            'display_page_links': DISPLAY_PAGE_LINKS,
            'is_paginated': paginator.count > paginator.per_page,
            'next_link_decorator': NEXT_LINK_DECORATOR,
            'page_obj': page_obj,
            'page_suffix': page_suffix,
            'pages': pages,
            'paginator': paginator,
            'previous_link_decorator': PREVIOUS_LINK_DECORATOR,
            'records': records,
        }
        if 'request' in context:
            getvars = context['request'].GET.copy()
            if 'page%s' % page_suffix in getvars:
                del getvars['page%s' % page_suffix]
            if len(getvars.keys()) > 0:
                new_context['getvars'] = "&%s" % getvars.urlencode()
            else:
                new_context['getvars'] = ''
        return new_context
    except (KeyError, AttributeError):
        return {}


register = Library()
register.tag('paginate', do_paginate)
register.tag('autopaginate', do_autopaginate)

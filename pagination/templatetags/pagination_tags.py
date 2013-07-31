try:
    set
except NameError:
    from sets import Set as set

from django import template
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from django.conf import settings
from pagination.paginator import CachedCountPaginator

register = template.Library()

DEFAULT_PAGINATION = getattr(settings, 'PAGINATION_DEFAULT_PAGINATION', 20)
DEFAULT_WINDOW = getattr(settings, 'PAGINATION_DEFAULT_WINDOW', 4)
DEFAULT_ORPHANS = getattr(settings, 'PAGINATION_DEFAULT_ORPHANS', 0)
INVALID_PAGE_RAISES_404 = getattr(settings,
    'PAGINATION_INVALID_PAGE_RAISES_404', False)

# def do_autopaginate(parser, token, PaginateNode=None):
#     """
#     Splits the arguments to the autopaginate tag and formats them correctly.
#     """
#     PaginateNode = AutoPaginateNode if not PaginateNode else PaginateNode
#     split = token.split_contents()
#     as_index = None
#     context_var = None
#     cache_counts = None
#     for i, bit in enumerate(split):
#         if bit == 'as':
#             as_index = i
#             continue
#         if bit == 'cache_counts':
#             cache_counts = i
#             continue
#     if as_index is not None:
#         try:
#             context_var = split[as_index + 1]
#         except IndexError:
#             raise template.TemplateSyntaxError("Context variable assignment " +
#                 "must take the form of {%% %r object.example_set.all ... as " +
#                 "context_var_name %%}" % split[0])
#         del split[as_index:as_index + 2]
#     if cache_counts is not None:
#         del split[cache_counts:cache_counts + 1]
#         PaginateNode = CachedAutoPaginateNode
#     if len(split) == 2:
#         return PaginateNode(split[1])
#     elif len(split) == 3:
#         return PaginateNode(split[1], paginate_by=split[2], 
#             context_var=context_var)
#     elif len(split) == 4:
#         try:
#             orphans = int(split[3])
#         except ValueError:
#             raise template.TemplateSyntaxError(u'Got %s, but expected integer.'
#                 % split[3])
#         return PaginateNode(split[1], paginate_by=split[2], orphans=orphans,
#             context_var=context_var)
#     else:
#         raise template.TemplateSyntaxError('%r tag takes one required ' +
#             'argument and one optional argument' % split[0])


# def cached_count_paginate(parser, token):
#     """
#     Caches Queryset counts to improve the performance of the built-in Django Paginator
#     """
#     return do_autopaginate(parser, token, PaginateNode=CachedAutoPaginateNode)


class AutoPaginateNode(template.Node):
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
        
        The paginator attribute has been added for Yipit customization to allow for 
        a custom paginator (YipitInfinitePaginator). The default is the django core Paginator
        object, which is what AutoPaginateNode used pre-forking.
    """
    def __init__(self, queryset_var, paginate_by=DEFAULT_PAGINATION,
        orphans=DEFAULT_ORPHANS, context_var=None, paginator=Paginator):
        self.queryset_var = template.Variable(queryset_var)
        if isinstance(paginate_by, int):
            self.paginate_by = paginate_by
        else:
            self.paginate_by = template.Variable(paginate_by)
        self.orphans = orphans
        self.context_var = context_var
        self.paginator = paginator

    def render(self, context):
        key = self.queryset_var.var
        value = self.queryset_var.resolve(context)
        if isinstance(self.paginate_by, int):
            paginate_by = self.paginate_by
        else:
            paginate_by = self.paginate_by.resolve(context)
        paginator = self.paginator(value, paginate_by)
        try:
            page_obj = paginator.page(context['request'].page)
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
        return u''


class CachedAutoPaginateNode(AutoPaginateNode):

    def __init__(self, queryset_var, paginate_by=DEFAULT_PAGINATION,
        orphans=DEFAULT_ORPHANS, context_var=None, paginator=CachedCountPaginator):
        
        super(CachedAutoPaginateNode, self).__init__(queryset_var, paginate_by=paginate_by,
            orphans=orphans, context_var=context_var, paginator=paginator)


def do_autopaginate(parser, token, PaginateNode=AutoPaginateNode):
    """
    Splits the arguments to the autopaginate tag and formats them correctly.
    """
    split = token.split_contents()
    as_index = None
    context_var = None
    cache_counts = None
    for i, bit in enumerate(split):
        if bit == 'as':
            as_index = i
            continue
        if bit == 'cache_counts':
            cache_counts = i
            continue
    if as_index is not None:
        try:
            context_var = split[as_index + 1]
        except IndexError:
            raise template.TemplateSyntaxError("Context variable assignment " +
                "must take the form of {%% %r object.example_set.all ... as " +
                "context_var_name %%}" % split[0])
        del split[as_index:as_index + 2]
    if cache_counts is not None:
        del split[cache_counts:cache_counts + 1]
        PaginateNode = CachedAutoPaginateNode
    if len(split) == 2:
        return PaginateNode(split[1])
    elif len(split) == 3:
        return PaginateNode(split[1], paginate_by=split[2], 
            context_var=context_var)
    elif len(split) == 4:
        try:
            orphans = int(split[3])
        except ValueError:
            raise template.TemplateSyntaxError(u'Got %s, but expected integer.'
                % split[3])
        return PaginateNode(split[1], paginate_by=split[2], orphans=orphans,
            context_var=context_var)
    else:
        raise template.TemplateSyntaxError('%r tag takes one required ' +
            'argument and one optional argument' % split[0])


def paginate(context, window=DEFAULT_WINDOW, hashtag=''):
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
        """
    try:
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_range = paginator.page_range
        # Calculate the record range in the current page for display.
        records = {'first': 1 + (page_obj.number - 1) * paginator.per_page}
        records['last'] = records['first'] + paginator.per_page - 1
        if records['last'] + paginator.orphans >= paginator.count:
            records['last'] = paginator.count
        # First and last are simply the first *n* pages and the last *n* pages,
        # where *n* is the current window size.
        first = set(page_range[:window])
        last = set(page_range[-window:])
        # Now we look around our current page, making sure that we don't wrap
        # around.
        current_start = page_obj.number-1-window
        if current_start < 0:
            current_start = 0
        current_end = page_obj.number-1+window
        if current_end < 0:
            current_end = 0
        current = set(page_range[current_start:current_end])
        pages = []
        # If there's no overlap between the first set of pages and the current
        # set of pages, then there's a possible need for elusion.
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            # If there is a gap of two, between the last page of the first
            # set and the first page of the current set, then we're missing a
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        # If there's no overlap between the current set of pages and the last
        # set of pages, then there's a possible need for elusion.
        if len(current.intersection(last)) == 0:
            second_list = list(last)
            second_list.sort()
            diff = second_list[0] - pages[-1]
            # If there is a gap of two, between the last page of the current
            # set and the first page of the last set, then we're missing a 
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            differenced = list(last.difference(current))
            differenced.sort()
            pages.extend(differenced)
        to_return = {
            'MEDIA_URL': settings.MEDIA_URL,
            'pages': pages,
            'records': records,
            'page_obj': page_obj,
            'paginator': paginator,
            'hashtag': hashtag,
            'is_paginated': paginator.count > paginator.per_page,
        }
        if 'request' in context:
            getvars = context['request'].GET.copy()
            if 'page' in getvars:
                del getvars['page']
            if len(getvars.keys()) > 0:
                to_return['getvars'] = "&%s" % getvars.urlencode()
            else:
                to_return['getvars'] = ''
        return to_return
    except KeyError, AttributeError:
        return {}


def tailless_paginate(context, window=DEFAULT_WINDOW, hashtag=''):
    try:
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_range = paginator.page_range
        # Calculate the record range in the current page for display.
        records = {'first': 1 + (page_obj.number - 1) * paginator.per_page}
        records['last'] = records['first'] + paginator.per_page - 1
        if records['last'] + paginator.orphans >= paginator.count:
            records['last'] = paginator.count

        middle = page_obj.number
        length = len(page_range)
        
        # If the current page is too close to the beginning or end, let us
        # pretend that the current page is at least 'window' length away
        if middle < window:
            middle = window 
        if middle > length - window:
            middle = length - window

        # Now we look around our current page, making sure that we don't wrap
        # around.
        current_start = middle-1-window
        
        #Increment current_start
        current_start += 1
        
        if current_start < 0:
            current_start = 0
        current_end = middle-1+window
        if current_end < 0:
            current_end = 0

        pages = []
        
        if (current_end > length - 2):
            current_end = length

        current = set(page_range[current_start:current_end])
        first = set(page_range[0:2])
        
        # If there's no overlap between the first set of pages and the current
        # set of pages, then there's a possible need for elusion.
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            # If there is a gap of two, between the last page of the first
            # set and the first page of the current set, then we're missing a
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        
        if (current_end < length):
            pages.append(None)

        to_return = {
            'MEDIA_URL': settings.MEDIA_URL,
            'pages': pages,
            'records': records,
            'page_obj': page_obj,
            'paginator': paginator,
            'hashtag': hashtag,
            'is_paginated': paginator.count > paginator.per_page,
        }
        if 'request' in context:
            getvars = context['request'].GET.copy()
            if 'page' in getvars:
                del getvars['page']
            if len(getvars.keys()) > 0:
                to_return['getvars'] = "&%s" % getvars.urlencode()
            else:
                to_return['getvars'] = ''
        return to_return
    except KeyError, AttributeError:
        return {}


register.inclusion_tag('pagination/yipit_pagination.html', takes_context=True)(
    paginate)
register.inclusion_tag('pagination/tailless_pagination.html', takes_context=True)(
    tailless_paginate)
register.tag('autopaginate', do_autopaginate)
# register.tag('cachedpaginate', cached_count_paginate)

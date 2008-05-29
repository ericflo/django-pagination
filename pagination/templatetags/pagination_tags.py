try:
    set
except NameError:
    from sets import Set as set
from django import template
from pagination.registration import get_registry, default_pagination
registry = get_registry()
from django.db.models.query import QuerySet
from django.core.paginator import QuerySetPaginator, InvalidPage
#from django.template.loader import render_to_string

register = template.Library()

def do_autopaginate(parser, token):
    split = token.split_contents()
    if len(split) == 1:
        return AutoPaginateNode()
    elif len(split) == 2:
        return AutoPaginateNode(queryset_var=split[1])
    else:
        raise template.TemplateSyntaxError('%r tag takes only one optional argument.' % split[0])

class AutoPaginateNode(template.Node):
    def __init__(self, queryset_var=None):
        if queryset_var:
            self.queryset_var = template.Variable(queryset_var)
        else:
            self.queryset_var = None

    def render(self, context):
        if self.queryset_var is not None:
            try:
                key = self.queryset_var.var
                value = self.queryset_var.resolve(context)
                model = value.model
                pagination = registry.get_for_model(model)
                if pagination is None:
                    pagination = default_pagination
                paginator = QuerySetPaginator(value, pagination)
                try:
                    page_obj = paginator.page(context['request'].page)
                except:
                    return u''
                context[key] = page_obj.object_list
                context['paginator'] = paginator
                context['page_obj'] = page_obj
                return u''
            except template.VariableDoesNotExist:
                pass
        for d in context:
            for key, value in d.iteritems():
                if issubclass(value.__class__, QuerySet):
                    model = value.model
                    pagination = registry.get_for_model(model)
                    if pagination is not None:
                        paginator = QuerySetPaginator(value, pagination)
                        try:
                            page_obj = paginator.page(context['request'].page)
                        except:
                            return u''
                        context[key] = page_obj.object_list
                        context['paginator'] = paginator
                        context['page_obj'] = page_obj
                        return u''
        return u''

def paginate(context, window=4):
    paginator = context['paginator']
    page_obj = context['page_obj']
    page_range = paginator.page_range
    first = set(page_range[:window])
    last = set(page_range[-window:])
    current_start = page_obj.number-1-window
    if current_start < 0:
        current_start = 0
    current_end = page_obj.number-1+window
    if current_end < 0:
        current_end = 0
    current = set(page_range[current_start:current_end])
    pages = []
    if len(first.intersection(current)) == 0:
        pages.extend(sorted(list(first)))
        pages.append(None)
        pages.extend(sorted(list(current)))
    else:
        pages.extend(sorted(list(first.union(current))))
    if len(current.intersection(last)) == 0:
        pages.append(None)
        pages.extend(sorted(list(last)))
    else:
        pages.extend(sorted(list(last.difference(current))))
    return { 
        'pages': pages,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.count > paginator.per_page,
    }
    
register.inclusion_tag('pagination/pagination.html', takes_context=True)(paginate)
register.tag('autopaginate', do_autopaginate)

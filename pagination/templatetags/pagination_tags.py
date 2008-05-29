try:
    set
except NameError:
    from sets import Set as set

def paginate(context, window=4):
    paginator = context['paginator']
    page_obj = context['page_obj']
    page_range = paginator.page_range
    first = set(page_range[:window])
    last_start = len(page_range)-window
    if last_start < 0:
        last_start = 0
    last = set(page_range[last_start:])
    current_start = page_obj.number-1-window
    if current_start < 0:
        current_start = 0
    current = set(page_range[current_start:page_obj.number-1+window])
    pages = []
    if len(first.intersection(current)) == 0:
        pages.extend(list(first))
        pages.append(None)
        pages.extend(list(current))
    else:
        pages.extend(first.union(current))
    if len(current.intersection(last)) == 0:
        pages.append(None)
        pages.extend(list(last))
    else:
        pages.extend(list(last.difference(current)))
    return { 
        'pages': pages,
        'page_obj': page_obj,
        'paginator': paginator,
    }
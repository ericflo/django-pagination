from django.conf import settings
DEFAULT_PAGINATION = getattr(settings, 'PAGINATION_DEFAULT_PAGINATION', 20)


def get_page(self):
    """
    A function which will be monkeypatched onto the request to get the current
    integer representing the current page.
    """
    try:
        return int(self.REQUEST['page'])
    except (KeyError, ValueError, TypeError):
        return 1
    
    
def get_perpage(self):
    try:
        self.session['perpage'] = int(self.REQUEST['perpage'])
        return self.session['perpage']
    except (KeyError, ValueError, TypeError):
        pass

    try:
        return int(self.session['perpage'])
    except (KeyError, ValueError, TypeError):
        return DEFAULT_PAGINATION
    
    
class PaginationMiddleware(object):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """
    def process_request(self, request):
        request.__class__.page = property(get_page)
        request.__class__.perpage = property(get_perpage)
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    class MiddlewareMixin:
        def __init__(self, get_response=None):
            self.get_response = get_response
            super().__init__()

        def __call__(self, request):
            response = None
            if hasattr(self, 'process_request'):
                response = self.process_request(request)
            response = response or self.get_response(request)
            if hasattr(self, 'process_response'):
                response = self.process_response(request, response)
            return response


def get_page(self):
    """
    A function which will be monkeypatched onto the request to get the current
    integer representing the current page.
    """
    try:
        return int(self.GET['page'])
    except (KeyError, ValueError, TypeError):
        return 1


class PaginationMiddleware(MiddlewareMixin):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """
    def process_request(self, request):
        request.__class__.page = property(get_page)

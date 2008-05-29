class PaginationMiddleware(object):
    def process_request(self, request):
        try:
            request.page = int(request['page'])
        except KeyError:
            request.page = 1
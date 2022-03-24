class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class BaseApp:
    def __init__(self, urls_list, fronts_list):
        self.urls_list = urls_list
        self.fronts_list = fronts_list

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.urls_list:
            view = self.urls_list[path]
        else:
            view = PageNotFound404()
        request = {}
        for front in self.fronts_list:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

from my_framework.framework_requests import GetRequests, PostRequests
import quopri


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

        request = {}
        request_method = environ['REQUEST_METHOD']
        request['method'] = request_method
        print(request_method)

        if request_method == 'GET':
            request_params = GetRequests().get_request_dict(environ)
            request['request_params'] = request_params
            converted_params = BaseApp.decode_data(request_params)
            print(f"We've got GET-parameters: {converted_params}")

        if request_method == 'POST':
            request_data = PostRequests().get_request_params(environ)
            request['data'] = request_data
            converted_data = BaseApp.decode_data(request_data)
            print(f"We've got POST-request. Request content:")
            for k, v in converted_data.items():
                print(f'{k}:', v)

        if path in self.urls_list:
            view = self.urls_list[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_list:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_data(data):
        """
        Функция принимает словарь с данными POST-запроса
        и переводит в байты с помощью функции decodestring библиотеки quopri
        :param data: данные в байтах
        :return:
        """
        decoded_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', " "), 'utf-8')
            decoded_str = quopri.decodestring(val).decode('utf-8')
            decoded_data[k] = decoded_str
        return decoded_data

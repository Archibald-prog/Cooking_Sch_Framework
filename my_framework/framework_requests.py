class GetRequests:

    @staticmethod
    def parse_request_data(data) -> dict:
        result = {}
        if data:
            # строку вида 'query=str.lower&opt=9'
            # превращаем в словарь вида {'query': 'str.lower', 'opt': '9'}
            for item in data.split('&'):
                key, val = item.split('=')
                result[key] = val
        return result

    @staticmethod
    def get_request_dict(environ) -> dict:
        query_string_data = environ['QUERY_STRING']
        request_dict = GetRequests.parse_request_data(query_string_data)
        return request_dict


class PostRequests:

    @staticmethod
    def parse_request_data(data) -> dict:
        result = {}
        if data:
            for item in data.split('&'):
                key, val = item.split('=')
                result[key] = val
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        """
        Функция возвращает тело запроса в байтах
        :param env: словарь environ
        :return:
        """
        content_length_data = env.get('CONTENT_LENGTH')
        if content_length_data:
            content_length = int(content_length_data)
        else:
            content_length = 0
        if content_length > 0:
            data = env['wsgi.input'].read(content_length)
        else:
            data = b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # Декодируем данные – получаем строку
            data_str = data.decode(encoding='utf-8')
            # Преобразуем строку в словарь
            result = self.parse_request_data(data_str)
        return result

    def get_request_params(self, environ) -> dict:
        # Получаем данные в байтах
        data = self.get_wsgi_input_data(environ)
        # Преобразуем байты в словарь
        data = self.parse_wsgi_input_data(data)
        return data

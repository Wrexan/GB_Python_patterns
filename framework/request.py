from urllib import parse


class Request:
    def __init__(self, environ: dict):
        self.headers = self._get_http_headers(environ)
        self.method = environ.get('REQUEST_METHOD')
        self.body = self._post_query_params(environ)
        self.query_params = self._get_query_params(environ)
        self.path = environ.get('PATH_INFO')
        self.client_ip4 = environ.get('REMOTE_ADDR')
        self.origin = environ.get('ORIGIN')

    def _get_http_headers(self, environ: dict):
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:]] = value
            #     print('HTTP:', key, value)
            # else:
            #     print('NOT HTTP:', key, value)
        return headers

    def _get_query_params(self, environ: dict):
        data = parse.unquote(environ.get('QUERY_STRING'))
        if not data:
            return
        return self._parse_query(data, '&')

    def _post_query_params(self, environ: dict):
        data = parse.unquote(environ.get('wsgi.input').read().decode("utf-8"))
        if not data:
            return
        return self._parse_query(data, '\r\n')

    def _parse_query(self, data: str, terminator: str):
        query_params = {}
        try:
            for pair in data.split(terminator):
                if not pair:
                    continue
                var, value = pair.split('=')
                if query_params.get(var):
                    query_params[var].append(value)
                else:
                    query_params[var] = value
        except Exception as e:
            print(f"ERROR: Can't parse request: {e}")
            return
        return query_params

from framework.request import Request
# from url import Url
# from views import Views
from url import links
# GET, POST, PUT, HEAD, DELETE, TRACE, OPTIONS, CONNECT, PATCH


class WSGI:
    # def __init__(self):
    # self.views = views
    # self.links = links
    # views = Views.view
    # links = links

    def app(self, environ, start_response):
        req = Request(environ)
        # links = links
        # print(f'{links=}')
        # print(f'{self.links=}')
        if req.method == 'GET':
            # print(f'{req.headers=}')
            # print(f'{req.body.read()=}')
            for url, method in links.items():
                # print(f'{url=} {method=} ')
                if req.path == url:
                    start_response('200 OK', [('Content-Type', 'text/html')])
                    # print(f'{method()=}')
                    return [bytes(f'{method()}', encoding='utf-8')]
        return [b'404']

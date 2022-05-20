from framework.wsgi import WSGI

server = WSGI()


def run(environ, start_response):
    return server.app(environ, start_response)

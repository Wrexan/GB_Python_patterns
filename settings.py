from framework.front_controller import Middleware
import database

MIDDLEWARE = (
    Middleware.answer_time,
    Middleware.cors
)
MIDDLEWARE_SETUP = {
    'cors_ip_whitelist': (
        '127.0.0.1',
        '0.0.0.0'
    ),
    'cors_ip_blacklist': (
    )
}
# Default 404 error page
PAGE_404 = ''

# How many page layers need injections. Default = 1. Deeper is slower.
# 0: page in index
# 1: page in page in index
DEEPNESS = 1

FRONTEND_PATH = 'frontend/'

DATABASE = database
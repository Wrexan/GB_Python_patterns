from framework.views import View
FRONTEND_PATH = 'frontend/'

FRONTEND_VARS = {
    '%index%': '"/index"',
    '%about%': '"/about"',
    '%courses%': '"/courses"',
    '%contacts%': '"/contacts"'
}
PAGE_TEMPLATE = 'main_template.html'

Home = View(FRONTEND_PATH, FRONTEND_VARS, PAGE_TEMPLATE)


def index(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('index.html')
    elif request.method == 'POST':
        page = Home.view('index.html')
        print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


def about(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('about.html')
    elif request.method == 'POST':
        page = Home.view('about.html')
        print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


def courses(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        if request.query_params is None:
            page = Home.view('courses.html')
        else:
            if 'edu_line' in request.query_params:
                print(request.query_params['edu_line'])
                page = Home.view('courses.html')
    elif request.method == 'POST':
        page = Home.view('courses.html')
        print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


def contacts(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('contacts.html')
    elif request.method == 'POST':
        page = Home.view('contacts.html')
        print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


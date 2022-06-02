from framework.views import View, app, debug
from database import db_get_line, db_get_lines, db_get_course, db_get_courses_by_line
FRONTEND_PATH = 'frontend/'

# Global vars. Will be changed for text in all pages.
# Useful for links.
FRONTEND_CONST = {
    '%index%': '"/index"',
    '%about%': '"/about"',
    '%courses%': '"/courses"',
    '%contacts%': '"/contacts"',
}
# Objects visible only for admin
FRONTEND_ADMIN_VARS = {
    '%admin_page%': '"/admin_page"',
    '%admin_panel%': 'Админка'
}
# How many page layers need injections. Default = 1. Deeper is slower.
# 0: page in index
# 1: page in page in index
DEEPNESS = 1

Home = View(FRONTEND_PATH, FRONTEND_CONST, FRONTEND_ADMIN_VARS, DEEPNESS)

Home.is_admin = True


@app('/index')
def index(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('index.html', {'content': 'main_page.html'})
    # elif request.method == 'POST':
    #     page = Home.view('index.html', {'content': 'main_page.html'})
    #     print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


@app('/about')
@debug
def about(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('index.html', {'content': 'about.html'})
    # elif request.method == 'POST':
    #     page = Home.view('index.html', {'content': 'about.html'})
    #     print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


@debug
def courses(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        if request.query_params is None:
            page = Home.view('index.html', {'content': 'courses_page.html',
                                            'edu_line1': db_get_line(1)['name'],
                                            'edu_line2': db_get_line(2)['name'],
                                            'edu_line3': db_get_line(3)['name'],
                                            'courses': 'courses_invitation.html'})
        else:
            if 'edu_line' in request.query_params:
                courses_of_line = db_get_courses_by_line(request.query_params["edu_line"])
                # print(f'{courses_of_line=}')
                page = Home.view('index.html', {'content': 'courses_page.html',
                                                'courses': 'courses.html',
                                                'edu_line1': db_get_line(1)['name'],
                                                'edu_line2': db_get_line(2)['name'],
                                                'edu_line3': db_get_line(3)['name'],
                                                'course': courses_of_line,
                                                'course_page': 'course_page.html',
                                                'course_form': 'course_form.html',
                                                'first_form_id': 1},
                                 request.query_params["edu_line"])
            if 'course_page' in request.query_params:
                course = db_get_course(request.query_params["course_page"])
                # print(f'{course=}')
                page = Home.view('index.html', {'content': 'course_page.html',
                                                'course': course},
                                 request.query_params["course_page"])
            if 'enroll_course' in request.query_params:
                course = db_get_course(request.query_params["enroll_course"])
                print(f'Клиент записан на {course["name"]}')
                page = Home.view('index.html', {'content': 'thank_for_enroll.html',
                                                'course': course})
                # page = Home.view('index.html', {'content': 'courses_page.html',
                #                                 'edu_line1': db_get_line(1)['name'],
                #                                 'edu_line2': db_get_line(2)['name'],
                #                                 'edu_line3': db_get_line(3)['name'],
                #                                 'course': course,
                #                                 'courses': 'thank_for_enroll.html'})
    elif request.method == 'POST':
        page = Home.view('courses.html')
        print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


def contacts(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('index.html', {'content': 'contacts.html'})
    elif request.method == 'POST':
        page = Home.view('index.html', {'content': 'contacts.html'})
        print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


def admin(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('index.html', {'content': 'admin_page.html'})
    # elif request.method == 'POST':
    #     page = Home.view('index.html', {'content': 'admin_page.html'})
    #     print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


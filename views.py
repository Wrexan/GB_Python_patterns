from framework.views import View
from database import db_get_line, db_get_lines, db_get_course, db_get_courses_by_line
FRONTEND_PATH = 'frontend/'

# Global vars. Will be changed for text in all pages.
# Useful for links.
FRONTEND_VARS = {
    '%index%': '"/index"',
    '%about%': '"/about"',
    '%courses%': '"/courses"',
    '%contacts%': '"/contacts"'
}
# How many page layers need injections. Default = 1. Deeper is slower.
# 0: page in index
# 1: page in page in index
DEEPNESS = 2

Home = View(FRONTEND_PATH, FRONTEND_VARS, DEEPNESS)


def index(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('index.html', {'content': 'main_page.html'})
    # elif request.method == 'POST':
    #     page = Home.view('index.html', {'content': 'main_page.html'})
    #     print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


def about(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Home.view('index.html', {'content': 'about.html'})
    # elif request.method == 'POST':
    #     page = Home.view('index.html', {'content': 'about.html'})
    #     print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


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
                                                'course_form': 'course_form.html'},
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


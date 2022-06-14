from database import DB
from framework.users import U
from framework.views import View, app, debug

# Global constants. Will be changed for text in all pages.
# Useful for links.
FRONTEND_CONST = {
    '%index%': '"javascript:;" onclick="url(/index);"',
    '%about%': '"/about"',
    '%courses%': '"/courses"',
    '%contacts%': '"/contacts"',
    '%login%': '"/login"',
    '%logout%': '"/logout"',
    '%register%': '"/register"',
    '%profile%': '"/profile"',
    '%admin%': '"/admin"',
}
# Objects visible only for admin
# FRONTEND_ADMIN_VARS = {
#     '%admin_page%': '"/admin_page"',
#     '%admin_panel%': 'Админка'
# }


Site = View(FRONTEND_CONST)
db = DB
db.db_precount_courses_for_lines()

users = U
Site.is_admin = True  # todo

# Global vars. Will be changed for data in all pages.
# Useful for changeable data that present in all (many) pages
Site.frontend_vars = {'is_admin': Site.is_admin,
                      'is_logged': False, }


@app('/index')
def index(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        print(f'{request.verified=}')
        page = Site.view(request, 'index.html', {'content': 'main_page.html',
                                                 'verified': request.verified[0],
                                                 'username': request.verified[1]})
    return page


@app('/about')
@debug
def about(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Site.view(request, 'index.html', {'content': 'about.html'})
    return page


@debug
def courses(request):
    if request.method == 'GET':
        # print(f'GET {request.query_params=}')
        line = '0'
        curr_line = 'Выберите направление обучения'
        if request.query_params is None:
            pass
        else:
            if 'course_page' in request.query_params:
                course = db.db_get_course(request.query_params["course_page"])
                # print(f'{course=}')
                return Site.view(request, 'index.html', {'content': 'courses/course_page.html',
                                                         'course': course},
                                 request.query_params["courses/course_page"])

            elif 'enroll_course' in request.query_params:
                course = db.db_get_course(request.query_params["enroll_course"])
                print(f'Клиент записан на {course["name"]}')
                return Site.view(request, 'index.html', {'content': 'courses/thank_for_enroll.html',
                                                         'course': course})

            if 'line' in request.query_params:
                line = request.query_params["line"]
                curr_line = db.db_get_line(line)
                curr_line = curr_line['name'] if curr_line else ''
            else:
                line = '0'
        # print(f'{line=}')
        # print(f'{db_count_curses_in_line(line)=}')
        return Site.view(request, 'index.html', {'content': 'form_page.html',
                                                 'forms': 'forms.html',
                                                 'curr_line': curr_line,
                                                 'lines': db.db_get_lines(line),
                                                 'course': db.db_get_courses_by_line(line),
                                                 'form_page': 'form_page.html',
                                                 'line_form': 'line_form.html',
                                                 'course_form': 'courses/course_form.html',
                                                 'page': 0},)
    elif request.method == 'POST':
        return Site.view(request, 'courses/courses.html')
        # print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return f'unsupported method {request.method}'


def contacts(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Site.view(request, 'index.html', {'content': 'contacts.html'})
    elif request.method == 'POST':
        page = Site.view(request, 'index.html', {'content': 'contacts.html'})
        # print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


@app('/admin')
def admin(request):
    page = f'unsupported method {request.method}'
    if request.method == 'GET':
        page = Site.view(request, 'index.html', {'content': 'admin_page.html',
                                                 'user_list': db.users})
    # elif request.method == 'POST':
    #     page = Site.view('index.html', {'content': 'admin_page.html'})
    #     print(f'==Got {request.method=} {request.query_params=} {request.body=}')
    return page


@app('/login')
def login(request):
    print(f'LOGIN GOT AUTH {request.method=} {request.query_params=} {request.act=} {request.auth=}')
    if request.method == 'GET':
        return Site.view(request, 'index.html', {'content': 'login.html'})
    elif request.method == 'POST':
        if request.act == 'login':
            ok, msg = users.login_user(request)
            if ok:
                return Site.view(request, 'index.html', {'content': 'main_page.html',
                                                         'msg': msg}, )
            else:
                return Site.view(request, 'index.html', {'content': 'login.html',
                                                         'msg': msg}, )
        else:
            return Site.view(request, 'index.html', {'content': 'login.html'})
    return f'unsupported method {request.method}'


@app('/register')
def admin(request):
    # print(f'REGISTER GOT {request.method=} {request.query_params=} {request.auth=} {request.body=}')
    if request.method == 'GET':
        return Site.view(request, 'index.html', {'content': 'register.html'})
    elif request.method == 'POST':
        if request.act == 'reg':
            ok, msg = users.create_user(request)
            if ok:
                ok, _ = users.login_user(request, reg_login=True)
                return Site.view(request, 'request, index.html', {'content': 'main_page.html',
                                                                  'msg': msg}, )
            else:
                return Site.view(request, 'index.html', {'content': 'register.html',
                                                         'msg': msg}, )
        else:
            return Site.view(request, 'index.html', {'content': 'register.html'})
            # print(f'Error registering user: {request.method=} {request.query_params=} {request.body=}')
    return f'unsupported method {request.method}'

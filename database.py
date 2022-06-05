def db_get_line(id):
    id = _to_int(id)
    for elem in database_course_lines:
        if elem['id'] == id:
            return elem
    return None


def db_get_lines(id):
    id = _to_int(id)
    lines = []
    for elem in database_course_lines:
        if elem['parent'] == id:
            lines.append(elem)
    return lines


def db_get_all_lines():
    return database_course_lines


def db_get_course(id):
    id = _to_int(id)
    for elem in database_courses:
        if elem['id'] == id:
            elem['type'] = db_get_type(elem['type'])
            # print(f'{elem=}')
            return elem
    return None


def db_get_courses_by_line(line):
    line = _to_int(line)
    res = [elem for elem in database_courses if elem['line'] == line]
    for elem in res:
        for t in database_course_types:
            if t['id'] == elem['type']:
                elem['type'] = t['name']
                break
    return res


def db_get_course_amt_by_line(line) -> int:
    # line = _to_int(line)
    count = 0
    for elem in database_courses:
        if elem['line'] == line:
            count = count + 1
    # print(f'{count=}')
    return count


# def db_precount_courses_for_lines():
#     for line in database_course_lines:
#         line['courses_in'] += db_count_curses_in_line(line['id'])


def db_count_curses_in_line_new(id):
    all_db_parent_ids = list(set([elem["parent"] for elem in database_course_lines]))  # "set" gets all unique ids
    counter = 0
    # sublevel_ids = []

    def recoursive(id):
        nonlocal counter
        for line in database_course_lines:
            if line["parent"] == id:
                counter += db_get_course_amt_by_line(line["id"])
                current_id = line["id"]
                # sublevel_ids.append(current_id)
                if current_id in all_db_parent_ids:
                    recoursive(current_id)
        return counter#, sublevel_ids
    return recoursive(id)


# def db_precount_courses_for_lines():
    # for line in database_course_lines:
        # line['courses_in'] += db_count_curses_in_line(line['id'])


    # def db_count_curses_in_line(id: int = 0, amt: int = 0) -> int:
    # # def db_count_curses_in_line(id: int, amt: int = 0) -> int:
    #     # id = _to_int(id)
    #     # print(f'NAME: {id} AMT:{amt}')
    #     for line in database_course_lines:
    #         if line['parent'] == id:
    #             amt_in_dother = db_get_course_amt_by_line(line["id"])
    #             amt += db_count_curses_in_line(line['id'], amt_in_dother)
    #             line['courses_in'] = amt_in_dother #+ amt
    #             print(f'NAME: {line["name"]} AMT:{amt} AMT_D:{amt_in_dother}')
    #     return amt
    #
    # db_count_curses_in_line()
    #
    # # for line in database_course_lines:
    # #         line['courses_in'] += db_count_curses_in_line(line['id'])

def db_precount_courses_for_lines():

    def db_count_curses_in_branch(_id: int = 0, amt: int = 0) -> int:
        for lin in database_course_lines:
            if lin['parent'] == _id:
                amt += db_count_curses_in_branch(lin['id'], lin['courses_in'])
                # print(f'NAME: {line["name"]} AMT:{amt} courses_in:{line["courses_in"]}')
        return amt

    for line in database_course_lines:
        amt_d = db_get_course_amt_by_line(line["id"])
        line['courses_in'] = amt_d
        # print(f'PRE -- NAME: {line["name"]} AMT_D:{amt_d}')
    for line in database_course_lines:
        line['courses_in'] += db_count_curses_in_branch(line['id'])

def db_get_type(id):
    # id = _to_int(id)
    for elem in database_course_types:
        if elem['id'] == id:
            return elem
    return database_course_types[0]['name']


def _to_int(var):
    # print(f'{type(var)=}')
    if not var:
        return 1
    return var if isinstance(var, int) else int(var)


database_course_types = (
    {'id': 1, 'name': 'онлайн'},
    {'id': 2, 'name': 'офлайн'},
)


database_course_lines = (
    {'id': 1, 'parent': 0, 'courses_in': 0, 'name': 'Программирование'},
    {'id': 2, 'parent': 0, 'courses_in': 0, 'name': 'Электроника'},
    {'id': 3, 'parent': 0, 'courses_in': 0, 'name': 'Учимся жить'},

    {'id': 4, 'parent': 1, 'courses_in': 0, 'name': 'Базовые знания'},
    {'id': 13, 'parent': 1, 'courses_in': 0, 'name': 'Логика'},
    {'id': 5, 'parent': 1, 'courses_in': 0, 'name': 'Языки высокого уровня'},
    {'id': 6, 'parent': 1, 'courses_in': 0, 'name': 'Языки низкого уровня'},

    {'id': 14, 'parent': 5, 'courses_in': 0, 'name': 'Python'},
    {'id': 15, 'parent': 5, 'courses_in': 0, 'name': 'Java'},
    {'id': 16, 'parent': 5, 'courses_in': 0, 'name': 'JavaScript'},
    {'id': 17, 'parent': 5, 'courses_in': 0, 'name': 'Kotlin'},

    {'id': 18, 'parent': 6, 'courses_in': 0, 'name': 'Assembler'},
    {'id': 19, 'parent': 6, 'courses_in': 0, 'name': 'C'},
    {'id': 20, 'parent': 6, 'courses_in': 0, 'name': 'C++'},


    {'id': 7, 'parent': 2, 'courses_in': 0, 'name': 'Базовые элементы и понятия'},
    {'id': 8, 'parent': 2, 'courses_in': 0, 'name': 'Схемотехника'},
    {'id': 9, 'parent': 2, 'courses_in': 0, 'name': 'Ремонт электроники'},

    {'id': 10, 'parent': 3, 'courses_in': 0, 'name': 'Добрые дела'},
    {'id': 11, 'parent': 3, 'courses_in': 0, 'name': 'Выгодные дела'},
    {'id': 12, 'parent': 3, 'courses_in': 0, 'name': 'Безделье'},
)

database_courses = (
    {
        'id': 1, 'line': 10, 'name': 'Как перевести бабушку через дорогу', 'img': 'img:старушка', 'type': 1,
        'short': 'Обучает обходительному поведению. Объясняет все риски при контакте с бабушками',
        'text': 'После прохождения данного курса вы больше не сможете устоять и проведете бабушку через дорогу'
    },
    {
        'id': 2, 'line': 10, 'name': 'Как уступить место в транспорте', 'img': 'img:трамвай', 'type': 1,
        'short': 'У вас пропадет желание садиться. Узнаете альтернативные способы передвижения',
        'text': 'После прохождения данного курса вы больше не сможете сидеть и научитесь ходить'
    },
    {
        'id': 3, 'line': 10, 'name': 'Как покормить голубей', 'img': 'img:голуби', 'type': 2,
        'short': 'Научит убегать от копов, бомжей и зомби. Дополнительно информация о птичьем ГРИППе',
        'text': 'После прохождения данного курса вы больше не захотите кормить голубей. Так же повысится выживаемость'
    },
    {
        'id': 4, 'line': 10, 'name': 'Как заставить себя пойти на выборы', 'img': 'img:галочка', 'type': 2,
        'short': 'Узнаете что такое выборы и влияют ли они на что-то в вашей стране',
        'text': 'После прохождения данного курса вы скорее всего смените гражданство. Если это еще возможно.'
    },
    {
        'id': 5, 'line': 10, 'name': 'Как не лениться делать уборку', 'img': 'img:веник', 'type': 1,
        'short': 'Обучает базовым навыкам владения роботом-пылесосом',
        'text': 'После прохождения данного курса вы без труда найдете кнопку включения'
    },
    {
        'id': 6, 'line': 11, 'name': 'Как приручить соседа', 'img': 'img:лицо соседа', 'type': 1,
        'short': 'Обучает обрастать полезными связями. Объясняет все риски при контакте с соседом',
        'text': 'После прохождения данного курса вы больше не сможете устоять и пригласите соседа выпить'
    },
    {
        'id': 7, 'line': 11, 'name': 'Как заработать миллион за 15 минут', 'img': 'img:777', 'type': 2,
        'short': 'Обучает как быстро заработать и перейти на курс ничегонеделанья',
        'text': 'После прохождения данного курса вы больше не сможете купить другие курсы'
    },
    {
        'id': 8, 'line': 14, 'name': 'Основы Python', 'img': 'img:69', 'type': 2,
        'short': 'Обучает всякой всячине',
        'text': 'После прохождения данного курса вы больше не сможете сесть за другие языки'
    },
    {
        'id': 9, 'line': 14, 'name': 'Продвинутый Питон', 'img': 'img:96', 'type': 2,
        'short': 'Обучает как типизировать руками, магическим методам и type-ам мира сия',
        'text': 'После прохождения данного курса вы сможете превращать 5 строк в 1.'
                'Но придется превращать 5 строк в 10 классов.'
    },
    {
        'id': 10, 'line': 14, 'name': 'Бог Питона', 'img': 'img:8', 'type': 2,
        'short': 'Обучает познанию сути всего',
        'text': 'После прохождения данного курса вы сможете написать "Hello World" '
                'без использования абстрактных классов.'
    },
    {
        'id': 11, 'line': 18, 'name': 'Как полюбить регистры', 'img': 'img:AX BX CX DX', 'type': 2,
        'short': 'Обучает как не заработать клаустрофобию в стеке',
        'text': 'После прохождения данного курса вы больше не сможете 1101 0110 1100'
    },
    {
        'id': 12, 'line': 19, 'name': 'Поход в музей', 'img': 'img:BORLAND', 'type': 2,
        'short': 'Исторический курс',
        'text': 'После прохождения данного курса вам стоит пройти Паскаль'
    },
    {
        'id': 13, 'line': 1, 'name': 'История программирования', 'img': 'img:АРИФМОМЕТР', 'type': 2,
        'short': 'Исторический курс как человечество пришло к созданию первого языка',
        'text': 'Программирование от хардвара до хардкода'
    },
    {
        'id': 14, 'line': 6, 'name': 'История машинного кода', 'img': 'img:ПЕРФАЛЕНТА', 'type': 2,
        'short': 'Исторический курс как человечество скатилось от машинного кода к первому языку',
        'text': 'Машинный код - личинка ассемблера. Ладно, мне просто надо много курсов для теста.'
    },
)
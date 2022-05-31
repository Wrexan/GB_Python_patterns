def db_get_line(id):
    id = _to_int(id)
    for elem in database_course_lines:
        if elem['id'] == id:
            return elem
    return None


def db_get_lines():
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
    {'id': 1, 'name': 'Добрые дела'},
    {'id': 2, 'name': 'Выгодные дела'},
    {'id': 3, 'name': 'Безделье'},
)

database_courses = (
    {
        'id': 1, 'line': 1, 'name': 'Как перевести бабушку через дорогу', 'img': '1', 'type': 1,
        'short': 'Обучает обходительному поведению. Объясняет все риски при контакте с бабушками',
        'text': 'После прохождения данного курса вы больше не сможете устоять и проведете бабушку через дорогу'
    },
    {
        'id': 2, 'line': 1, 'name': 'Как уступить место в транспорте', 'img': '2', 'type': 1,
        'short': 'У вас пропадет желание садиться. Узнаете альтернативные способы передвижения',
        'text': 'После прохождения данного курса вы больше не сможете сидеть и научитесь ходить'
    },
    {
        'id': 3, 'line': 1, 'name': 'Как покормить голубей', 'img': '3', 'type': 2,
        'short': 'Научит убегать от копов, бомжей и зомби. Дополнительно информация о птичьем ГРИППе',
        'text': 'После прохождения данного курса вы больше не захотите кормить голубей. Так же повысится выживаемость'
    },
    {
        'id': 4, 'line': 1, 'name': 'Как заставить себя пойти на выборы', 'img': '4', 'type': 2,
        'short': 'Узнаете что такое выборы и влияют ли они на что-то в вашей стране',
        'text': 'После прохождения данного курса вы скорее всего смените гражданство. Если это еще возможно.'
    },
    {
        'id': 5, 'line': 1, 'name': 'Как не лениться делать уборку', 'img': '5', 'type': 1,
        'short': 'Обучает базовым навыкам владения роботом-пылесосом',
        'text': 'После прохождения данного курса вы без труда найдете кнопку включения'
    },
    {
        'id': 6, 'line': 2, 'name': 'Как приручить соседа', 'img': 'лицо соседа', 'type': 1,
        'short': 'Обучает обрастать полезными связями. Объясняет все риски при контакте с соседом',
        'text': 'После прохождения данного курса вы больше не сможете устоять и пригласите соседа выпить'
    },
    {
        'id': 7, 'line': 2, 'name': 'Как заработать миллион за 15 минут', 'img': '777', 'type': 2,
        'short': 'Обучает как быстро заработать и перейти на курс ничегонеделанья',
        'text': 'После прохождения данного курса вы больше не сможете купить другие курсы'
    },
)
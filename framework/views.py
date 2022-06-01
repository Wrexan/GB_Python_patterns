import sys, os


class View:
    def __init__(self,
                 frontend_path: str = 'frontend',
                 frontend_vars: dict = None,
                 frontend_admin_vars: dict = None,
                 deepness: int = 1):
        self.frontend_path = frontend_path
        self.frontend_vars = frontend_vars
        self.frontend_admin_vars = frontend_admin_vars
        self.deepness = deepness
        self.is_admin = False

    def view(self, page_file: str = 'index.html', injections=None, query_params=None):
        if injections is None:
            injections = {}
        if query_params is None:
            query_params = {}
        try:
            with open(f'{self.frontend_path}{page_file}', 'r') as file:
                data = file.read().replace('\n', '').replace('    ', ' ')
            # Заменяем переменные на содержимое из внешних файлов
            # if injections:
            #     for inj_name, inj_file in injections.items():
            data, _ = self._just_inject_in_that_file(data, injections, query_params, page_file)
            # data = self._just_inject_that_file(data, inj_name, inj_file)
            # Заменяем переменные на ссылки пользователя
            for var, link in self.frontend_vars.items():
                data = data.replace(var, link)
            for var, link in self.frontend_admin_vars.items():
                data = data.replace(var, link if self.is_admin else '')

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{fname}[{exc_tb.tb_lineno}]ERROR: while parsing view: ({page_file=}) {e}')
            return page_file
        return data

    # Костыли с рекурсией. Нагугленные способы импорта на сервере не работают
    def _just_inject_in_that_file(self, html_data, injections, query_params, file, num: int = 0):
        try:
            stopper = 0
            layer = 0
            inj_end = 0
            data = str(html_data) if isinstance(html_data, int) else html_data
            while layer < self.deepness:
                # print(f'Using layer {layer} of {self.deepness}')
                inj_start = data.find('{{', inj_end)
                if inj_start >= 0:
                    inj_end = data.find('}}', inj_start)
                    if inj_end == -1:
                        raise Exception(f'ERROR: not found "}}" in {file}')
                    inj_var = data[inj_start + 2: inj_end]
                    if len(inj_var) <= 1:
                        continue
                    # print(f'{inj_var=} {inj_start=} {inj_end=}')
                    # CYCLES. If * found, then content will repeat
                    cycle_pos = inj_var.find('*')
                    if cycle_pos >= 0:
                        cycle_end = data.find('{{*}}', inj_end)
                        cycle_data = data[inj_end + 2:cycle_end]
                        cycles = int(inj_var[cycle_pos + 1:])
                        cycle_var = inj_var[:cycle_pos]
                        if cycle_var.isdigit():
                            cycle_var = int(cycle_var)
                        elif cycle_var in injections.keys():
                            cycle_var = injections[cycle_var]
                        cycles_data = ''
                        # print(f'{inj_var=} {cycles=} {cycle_var=} {cycle_data=} ')
                        for i in range(0, cycles):
                            # print(f'cycle start: {i}  id:{cycle_var + i}')
                            cd, stopper = self._just_inject_in_that_file(cycle_data, injections, query_params,
                                                                        file, cycle_var + i)
                            cycles_data += cd
                            if stopper:
                                break
                            # print(f'cycle end: {i} {cycle_data=}')
                        inj_end = cycle_end + 3
                        data = data[:inj_start] + cycles_data + data[inj_end + 2:]
                        # print(f'CYCLES ENDED: {data=}')
                        continue
                    inj_arg, key = None, None

                    # if injections not empty:
                    if inj_var in injections.keys():
                        # If inj_var is key, inject directly
                        inj_arg = injections[inj_var]
                    else:

                        # If : found, then injection parse dict
                        dot_pos = inj_var.find(':')
                        if dot_pos >= 0:
                            obj = inj_var[:dot_pos]
                            key = inj_var[dot_pos + 1:]
                            # print(f'{key=} {arg=}')
                            if obj in injections.keys():
                                inj_arg = injections[obj]

                        # If # found, then get number
                        dot_pos = inj_var.find('#')
                        if dot_pos >= 0:
                            obj = inj_var[:dot_pos]
                            repeater = inj_var[dot_pos + 1:]
                            if repeater.isdigit():
                                num = int(repeater)
                            # elif repeater in injections.keys():
                            #     num = injections[repeater]
                            # print(f'{key=} {num=}')
                            if obj in injections.keys():
                                inj_arg = injections[obj]
                    # print(f'{inj_var=} {type(inj_arg)=}')
                    # print(f'{inj_arg=}')
                    if inj_arg:
                        file = inj_arg
                        if isinstance(inj_arg, str):
                            if inj_arg[-5:] == '.html':  # If str.html, then filename
                                inj_data = self._open_file(f'{self.frontend_path}{inj_arg}')
                            else:
                                inj_data = inj_arg
                        elif isinstance(inj_arg, list):
                            if num <= len(inj_arg):
                                # print(f'{num=} {len(inj_arg)=} {inj_arg[num - 1]["id"]=}')
                                inj_data = inj_arg[num - 1][key]
                                if num == len(inj_arg):
                                    stopper = 1
                            # print(f'{inj_arg[num][arg]=}')
                            else:
                                inj_data = ''

                        elif isinstance(inj_arg, dict):
                            if key in inj_arg:
                                inj_data = inj_arg[key]
                        elif isinstance(inj_arg, tuple):
                            print('tuple')
                        else:
                            print(f'ATTENTION: unknown type var: ({inj_var=} {type(inj_arg)=})'
                                  f' in ({file if isinstance(file, str) else "injection"})')
                            inj_data = ''
                    elif inj_var[-5:] == '.html':  # If not variable, then filename
                        inj_data = self._open_file(f'{self.frontend_path}{inj_var}')
                    else:
                        print(f'ATTENTION: unused var: ({inj_var=}) in ({file if isinstance(file, str) else "injection"})')
                        inj_data = ''
                    if layer < self.deepness:
                        inj_data, _ = self._just_inject_in_that_file(inj_data, injections, query_params, file, num)
                    data = data[:inj_start] + inj_data + data[inj_end + 2:]
                    # print(f'{data =}')
                    # print(f'{inj_var=} {inj_file=}')
                else:
                    layer += 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f'{fname}[{exc_tb.tb_lineno}]ERROR: while parsing view: ({file}) {e}')
        return data, stopper

    def _open_file(self, path):
        with open(path, 'r') as file:
            return file.read().replace('\n', '').replace('    ', ' ')

    def path(self, file_name: str):
        return f'{self.frontend_path}{file_name}'



class View:
    def __init__(self,
                 frontend_path: str = 'frontend',
                 frontend_vars: dict = None,
                 deepness: int = 1):
        self.frontend_path = frontend_path
        self.frontend_vars = frontend_vars
        self.deepness = deepness

    def view(self, page_file: str = 'index.html', injections=None, params=None):
        if injections is None:
            injections = {}
        if params is None:
            params = {}
        try:
            with open(f'{self.frontend_path}{page_file}', 'r') as file:
                data = file.read().replace('\n', '').replace('    ', ' ')
            # Заменяем переменные на содержимое из внешних файлов
            # if injections:
            #     for inj_name, inj_file in injections.items():
            data = self._just_inject_in_that_file(data, injections, params, page_file)
            # data = self._just_inject_that_file(data, inj_name, inj_file)
            # Заменяем переменные на ссылки пользователя
            for var, link in self.frontend_vars.items():
                data = data.replace(var, link)
        except Exception as e:
            print(f'ERROR: while parsing view: ({page_file=}) {e}')
            return page_file
        return data

    # Костыли с рекурсией. Нагугленные способы импорта на сервере не работают
    def _just_inject_in_that_file(self, data, injections, params, file, num: int = 0):
        layer = 0
        inj_end = 0
        # num = 0
        # key = ''
        while layer < self.deepness:
            # print(f'Using layer {layer} of {self.deepness}')
            inj_start = data.find('{{', inj_end)
            if inj_start >= 0:
                inj_end = data.find('}}', inj_start)
                if inj_end == -1:
                    raise Exception(f'ERROR: not found "}}" in {file}')
                inj_var = data[inj_start + 2: inj_end]
                if len(inj_var) <= 1:
                    # inj_end = inj_start + 5
                    continue
                # inj_end = inj_start + 2
                # print(f'{inj_var=} {inj_start=} {inj_end=}')
                # cycle_pos = inj_var.find('*')
                # if cycle_pos >= 0:  # If * found, then injection will repeat
                #     cycle_end = data.find('{{*}}', inj_end)
                #     cycles = int(inj_var[:cycle_pos])
                #     cycle_var = inj_var[inj_repeat + 1:]
                #
                #     # print(f'{inj_repeat=}')
                #     new_inj_var = inj_var[:inj_repeat]
                #     # print(f'{inj_var=}')
                #     inj_repeat = int(inj_var[inj_repeat + 1:])
                #     # print(f'{inj_repeat=}')
                #     inj_var = new_inj_var
                inj_arg = None
                # if injections:
                if inj_var in injections.keys():
                    inj_arg = injections[inj_var]
                else:
                    dot_pos = inj_var.find(':')
                    if dot_pos >= 0:  # If . found, then injection parse dict
                        key = inj_var[:dot_pos]
                        arg = inj_var[dot_pos + 1:]
                        # print(f'{key=} {arg=}')
                        if key in injections.keys():
                            # print(f'{injections=}')
                            inj_arg = injections[key]
                            # print(f'{inj_arg=}')
                    dot_pos = inj_var.find('#')
                    if dot_pos >= 0:  # If . found, then injection parse dict
                        key = inj_var[:dot_pos]
                        num = int(inj_var[dot_pos + 1:])
                        # print(f'{key=} {num=}')
                        if key in injections.keys():
                            # print(f'{injections=}')
                            inj_arg = injections[key]
                            # print(f'{inj_arg=}')
                # print(f'{inj_var=} {inj_arg=} {type(inj_arg)=}')
                if inj_arg:
                    # inj_arg = injections[inj_var]
                    file = inj_arg
                    # print(f'{inj_var=} {inj_arg=} {type(inj_arg)=}')
                    if isinstance(inj_arg, str):
                        if inj_arg[-5:] == '.html':  # If str.html, then filename
                            inj_data = self._open_file(f'{self.frontend_path}{inj_arg}')
                        else:
                            inj_data = inj_arg
                    elif isinstance(inj_arg, list):
                        if num < len(inj_arg):
                            # print(f'{num=} {inj_arg[num]["id"]=}')
                            inj_data = inj_arg[num][arg]
                            # print(f'{inj_arg[num][arg]=}')
                        else:
                            inj_data = ''

                    elif isinstance(inj_arg, dict):
                        print('dict')
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
                    # raise Exception
                    # continue

                if layer < self.deepness:
                    inj_data = self._just_inject_in_that_file(inj_data, injections, params, file, num)
                data = data[:inj_start] + inj_data + data[inj_end + 2:]
                # print(f'{data =}')
                # print(f'{inj_var=} {inj_file=}')
            else:
                layer += 1
        return data

    def _open_file(self, path):
        with open(path, 'r') as file:
            return file.read().replace('\n', '').replace('    ', ' ')

    def path(self, file_name: str):
        return f'{self.frontend_path}{file_name}'


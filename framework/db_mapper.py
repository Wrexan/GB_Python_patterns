import os
import sys
import sqlite3
import threading
from settings import DATABASE_PATH_FILE

connection = sqlite3.connect(DATABASE_PATH_FILE)


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()
        try:
            connection.commit()
            # del self
        except Exception as e:
            print(f'ERROR: {e}')
            # raise Exception(e.args)

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @classmethod
    def new_current(cls):
        cls.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Row):
            # print(f'Returning Registry {obj.table.table_name}')
            return obj.table  # Table(connection, 'person')  #


class DomainObject:
    def to_create(self):
        UnitOfWork.get_current().register_new(self)

    def to_edit(self):
        UnitOfWork.get_current().register_dirty(self)

    def to_delete(self):
        UnitOfWork.get_current().register_removed(self)


class Row(DomainObject):
    def __init__(self, table, row: dict):
        self.id = 0
        for key in row.keys():
            self.__setattr__(key, row[key])
        self.table = table
        self.to_create()

        # self.username = username
        # self.first_name = first_name
        # self.last_name = last_name
        # self.email = email
        # self.tel = tel


class Table:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """
    def __init__(self, table_name, fields, create=False):
        self.table_name = table_name
        self.fields = fields
        self.connection = connection
        self.cursor = connection.cursor()
        if create:
            self.create_table()

    def __str__(self):
        return self.table_name

    def create_table(self):
        self.cursor.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';''')
        table = self.cursor.fetchone()
        if not table:  # and self.cursor.fetchone()[0] == 0:
            print(f'Creating table {self.table_name}="{",".join("{} {}".format(*i) for i in self.fields.items())}"')

            self.cursor.execute(
                f"CREATE TABLE {self.table_name}({','.join('{} {}'.format(*i) for i in self.fields.items())});")
        else:
            print(f'Table {self.table_name} already exist')

    def find_by_id(self, id):
        print(f'Searching for {id} in {self}')
        result_columns = self.cursor.fetchone()
        statement = f"SELECT * FROM {self.table_name} WHERE ID=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        # print(f'{result=} {result_columns=} ')
        # print(f'{self.__dict__=}')
        if result:
            r = dict(zip(self.fields, result))
            # print(f'{r=}')
            return Row(self, r)
        return
        #     raise Exception(f'record with id={id} not found')

    def insert(self, row):
        print(f'Inserting {row.__dict__} in {row.table}')
        # statement = "INSERT INTO PERSON (USERNAME, FIRSTNAME, LASTNAME) VALUES (?, ?, ?)"
        statements, values, values_q = self._unpack_dict_insert(row)
        statement = f'''INSERT INTO {self.table_name} ({statements}) VALUES ({values_q})'''
        self.cursor.execute(statement, values)

    def update(self, row):
        print(f'Updating {row.id} in {row.table}')
        # statement = '''UPDATE PERSON SET USERNAME=?, FIRSTNAME=?, LASTNAME=? WHERE ID=?'''
        statements, values = self._unpack_dict_update(row)
        statement = f'''UPDATE {self.table_name} SET {statements} WHERE ID=?'''
        self.cursor.execute(statement, values)

    def delete(self, person):
        print(f'Deleting for {person.id} in {person.table}')
        statement = "DELETE FROM PERSON WHERE ID=?"
        self.cursor.execute(statement, (person.id,))

    @staticmethod
    def _unpack_dict_insert(_dict: dict):
        _statements = ''
        _values = []
        _values_q = ''
        for _k, _v in _dict.__dict__.items():
            if _k != 'table' and _k != 'id':
                _statements = f'{_statements}{_k}, '
                _values.append(_v)
                _values_q = f'{_values_q}?, '
        return _statements[:-2], _values, _values_q[:-2]

    @staticmethod
    def _unpack_dict_update(_dict: dict):
        _statements = ''
        _values = []
        _id = _dict.__dict__['id']
        for _k, _v in _dict.__dict__.items():
            if _k != 'table' and _k != 'id':
                _statements = f'{_statements}{_k}=?, '
                _values.append(_v)
        _values.append(_id)
        return _statements[:-2], _values



# with open('patterns.sqlite', 'r') as sqlite_file:
#     sql_script = sqlite_file.read()
# person_mapper = Table(connection, 'person')


# TEST
if __name__ == '__main__':
    # person1 = Person('Vasa', 'Pupken')
    # person2 = Person('Petia', 'Piatochkin')
    # person_mapper.insert(person1)
    # person_mapper.insert(person2)
    # person_1 = person_mapper.find_by_id(1)
    # person_2 = person_mapper.find_by_id(2)
    # print(person_1.__dict__)
    # print(person_2.__dict__)

    # users_fields = '''
    #     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    #     username VARCHAR (32) NOT NULL UNIQUE,
    #     password VARCHAR (44) NOT NULL,
    #     token VARCHAR (32),
    #     tel VARCHAR (16)
    #     '''

    users_fields = {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE',
        'username': 'VARCHAR (32) NOT NULL UNIQUE',
        'password': 'VARCHAR (44) NOT NULL',
        'token': 'VARCHAR (32)',
        'tel': 'VARCHAR (16)'
    }

    try:
        UnitOfWork.new_current()
        users = Table('users', users_fields, True)

        new_person_1 = Row(users, {'username': 'Basil', 'password': 'juAevLtnbBX1ZSzf7VbqHsxwAgRmtNdvLWzpsfEEuzE=',
                                   'token': '', 'tel': '555-55-55'})
        # new_person_1.mark_new()
        new_person_2 = Row(users, {'username': 'Peter', 'password': 'S//u5C6dqSdsWPyTTkXKwzm2CTaExAAnn4UtIcBs3Ho=',
                                   'token': '', 'tel': '555-55-55'})
        # new_person_2.mark_new()
        UnitOfWork.get_current().commit()
        exists_person_1 = users.find_by_id(1)
        # exists_person_1.to_edit()
        print(exists_person_1.username)

        UnitOfWork.new_current()
        exists_person_1.username += ' Senior'
        print(exists_person_1.username)
        exists_person_1.to_edit()
        # exists_person_2 = persons.find_by_id(2)
        # exists_person_2.mark_removed()
        print(UnitOfWork.get_current().__dict__)
        UnitOfWork.get_current().commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f'{fname}[{exc_tb.tb_lineno}]ERROR: {UnitOfWork.get_current()=} {e.args}')
    finally:
        UnitOfWork.set_current(None)
        print(UnitOfWork.get_current())

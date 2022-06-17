import sqlite3


# class Table:
#     def __init__(self, columns: dict):
#         for key in columns.keys():
#             self.__setattr__(key, columns[key])
#
#         cur.execute(f'CREATE TABLE {self.__name__}('
#                     f'')

# con = sqlite3.connect('temp.db')
# cur = con.cursor()
#
# cur.execute()
#
# db_users = Table({'username': 'Vasa'})
#
# print(dir(db_users))
# print(f'{db_users.username=}')

class Person:
    def __init__(self, username, first_name='', last_name='', email='', tel='', id_person=0):
        self.id_person = 0
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.tel = tel


class PersonMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """
    def __init__(self, connection, table_name):
        self.connection = connection
        self.cursor = connection.cursor()
        self.create_table(table_name)

    def create_table(self, table_name):
        self.cursor.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';''')
        f = self.cursor.fetchone()
        print(f'{f=}')
        if not f:  # and self.cursor.fetchone()[0] == 0:
            print(f'Creating table {table_name}')
            self.cursor.execute(f'''
            CREATE TABLE {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                username VARCHAR (32) NOT NULL UNIQUE,
                lastname VARCHAR (32),
                firstname VARCHAR (32)
            );''')
        else:
            print(f'Table {table_name} already exist')

    def find_by_id(self, id):
        statement = "SELECT ID, USERNAME, FIRSTNAME, LASTNAME FROM PERSON WHERE ID=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Person(*result)
        else:
            raise Exception(f'record with id={id} not found')

    def insert(self, person):
        statement = "INSERT INTO PERSON (USERNAME, FIRSTNAME, LASTNAME) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (person.username, person.first_name, person.last_name))
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)

    def update(self, person):
        statement = "UPDATE PERSON SET USERNAME=?, FIRSTNAME=?, LASTNAME=? WHERE ID=?"
        self.cursor.execute(statement, (person.username, person.first_name, person.last_name, person.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)

    def delete(self, person):
        statement = "DELETE FROM PERSON WHERE ID=?"
        self.cursor.execute(statement, (person.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise Exception(e.args)






connection = sqlite3.connect('patterns.db')
# with open('patterns.sqlite', 'r') as sqlite_file:
#     sql_script = sqlite_file.read()
person_mapper = PersonMapper(connection, 'person')

if __name__ == '__main__':
    person1 = Person('Vasa', 'Pupken')
    person2 = Person('Petia', 'Piatochkin')
    person_mapper.insert(person1)
    person_mapper.insert(person2)
    person_1 = person_mapper.find_by_id(1)
    person_2 = person_mapper.find_by_id(2)
    print(person_1.__dict__)
    print(person_2.__dict__)

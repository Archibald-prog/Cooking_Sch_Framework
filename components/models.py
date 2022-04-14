import quopri
from copy import deepcopy
from sqlite3 import connect
from components.behavioral_patterns import FileWriter, Subject
from components.unit_of_work import DomainObject


# Класс "Абстрактный пользователь"
class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


# Класс "Фабрика пользователей"
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        # возвращаем объект кл. Student или Teacher
        # в зависимости от переданного аргумента
        return cls.types[type_](name)


# Прототип - Курс
class CoursePrototype:
    def clone(self):
        return deepcopy(self)


# Класс-Курс
class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        # Добавляем объект кл. Course
        # в список курсов данной категории
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# Класс-Интерактивный курс
class InteractiveCourse(Course):
    pass


# Класс-Курс в записи
class RecordCourse(Course):
    pass


# Класс-Фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        # возвращаем объект InteratctiveCourse или RecordCourse
        # в зависимости от переданного аргумента type_
        return cls.types[type_](name, category)


# Класс-Категория
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    # возвращает число курсов данной категории
    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# Интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    # аргумент category передаем,
    # если создаваемая категория явл. подкатегорией
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        # читаем поле id
        # у всех элем-в списка Enginge().categories
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)

class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

connection = connect('project.sqlite')

class CourseMapper:
    pass

class CategoryMapper:
    pass

# Класс Реестр
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        # 'course': CourseMapper,
        # 'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)


    # позволяет избежать блоков if,
    # если в словаре mappers несколько ключей
    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')

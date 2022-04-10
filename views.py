from datetime import date

from my_framework.templator import render
from components.models import Engine, Logger
from components.structural_patterns import AppRoute, Debug
from components.behavioral_patterns import ListView, CreateView, TemplateView, \
    EmailNotifier, BaseSerializer, SmsNotifier, ConsoleWriter, FileWriter

site = Engine()
logger = Logger('main', ConsoleWriter())
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
routes = {}


# Главная страница
@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories, datetime=request.get('datetime', None))


# Страница "О проекте"
@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', data=date.today())


# Страница "Расписание"
@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study_programs.html', data=date.today())


# Страница 404
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# "Список курсов"
@AppRoute(routes=routes, url='/course_list/')
class CoursesList:
    def __call__(self, request):
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            # передаем в шаблон список курсов данной категории,
            # ее имя, id, и список курсов по всем категориям
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    full_course_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# Класс-контроллер - Страница "Создать курс"
@AppRoute(routes=routes, url='/create_course/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

                site.courses.append(course)

            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                print(f'ахх {request}')
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'

# Страница "Список студентов" - CBV
@AppRoute(routes=routes, url='/student_list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'

# Страница "Создать студента" - CBV
@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)

# Страница "Добавление студента на курс"
@AppRoute(routes=routes, url='/add_student/')
class AddStudentToCourse(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        # берем метод из род. класса
        # и получаем пустой словарь
        context = super().get_context_data()
        # создаем в словаре ключи 'courses' и 'students'
        # значение ключа берем из движка Engine
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()


# Страница "Создать категорию"
@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':

            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            # category_id = data.get('category_id')
            category = None
            # if category_id:
            #     category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            return '200 OK', render('categories_list.html',
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories
                                    )


# Список категорий CBV
@AppRoute(routes=routes, url='/categories_list/')
class CategoryList(ListView):
    queryset = site.categories
    template_name = 'categories_list.html'


# Страница "Контакты" CBV
@AppRoute(routes=routes, url='/contact/')
class Contact(TemplateView):
    template_name = 'contact.html'


# Страница "Рецепты" - CBV
@AppRoute(routes=routes, url='/recipes_page/')
class RecipesPage(TemplateView):
    template_name = 'recipes.html'



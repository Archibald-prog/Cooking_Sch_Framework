from my_framework.templator import render
from components.models import Engine
from datetime import date
from components.structural_patterns import AppRoute, Debug

site = Engine()
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


# "Список категорий"
@AppRoute(routes=routes, url='/categories_list/')
class CategoryList:
    def __call__(self, request):
        return '200 OK', render('categories_list.html',
                                objects_list=site.categories)


# Страница "Контакты"
@AppRoute(routes=routes, url='/contact/')
class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', datetime=request.get('datetime', None))

# Страница "Рецепты"
@AppRoute(routes=routes, url='/recipes_page/')
class RecipesPage:
    def __call__(self, request):
        return '200 OK', render('recipes.html', datetime=request.get('datetime', None))



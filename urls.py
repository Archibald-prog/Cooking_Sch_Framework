import datetime
# from views import Index, Contact, CoursesList, CreateCourse, CategoryList, \
#     CreateCategory, StudyPrograms, RecipesPage, About


# блок FC
def first_front(request):
    request['datetime'] = datetime.datetime.now()


def second_front(request):
    request['key'] = 'key'


fronts = [first_front, second_front]

# routes = {
#     '/': Index(),
#     '/contact/': Contact(),
#     '/about/': About(),
#     '/recipes_page/': RecipesPage(),
#     '/course_list/': CoursesList(),
#     '/create_course/': CreateCourse(),
#     '/categories_list/': CategoryList(),
#     '/create_category/': CreateCategory(),
#     '/study_programs/': StudyPrograms(),
# }

import datetime
from views import Index, About, Contact, Examples, AnotherPage, Page


# блок FC
def first_front(request):
    request['datetime'] = datetime.datetime.now()


def second_front(request):
    request['key'] = 'key'


fronts = [first_front, second_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contact/': Contact(),
    '/examples/': Examples(),
    '/another_page/': AnotherPage(),
    '/page/': Page(),
}

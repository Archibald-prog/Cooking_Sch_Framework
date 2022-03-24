from my_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', datetime=request.get('datetime', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', datetime=request.get('datetime', None))


class AnotherPage:
    def __call__(self, request):
        return '200 OK', render('another_page.html', datetime=request.get('datetime', None))


class Examples:
    def __call__(self, request):
        return '200 OK', render('examples.html', datetime=request.get('datetime', None))

class Page:
    def __call__(self, request):
        return '200 OK', render('page.html', datetime=request.get('datetime', None))

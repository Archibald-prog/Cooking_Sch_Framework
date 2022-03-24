from wsgiref.simple_server import make_server
from my_framework.main import BaseApp
from urls import routes, fronts

app = BaseApp(routes, fronts)

with make_server('', 8080, app) as httpd:
    print("Starting on port 8080...")
    httpd.serve_forever()

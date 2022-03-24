from jinja2 import Template
from os.path import join


def render(template_name, folder='templates', **kwargs):
    file_path = join(folder, template_name)
    with open(file_path, encoding='utf-8') as f:
        # шаблон в виде строки передаем в класс jinja2.Template
        template = Template(f.read())
    # вызываем у шаблона встроенную функцию render
    # передаем в нее словарь с динамическими данными
    return template.render(**kwargs)

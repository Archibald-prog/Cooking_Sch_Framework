from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Функция выполняет рендеринг шаблонов
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)

    # Загрузчик можно передать в блок __init__
    # класса Environment при создании экземпляра.
    # По умолчанию атрибут loader=None

    # loader = FileSystemLoader(folder)
    # env = Environment(loader=loader)
    # template = env.get_template(template_name)
    # return template.render(**kwargs)

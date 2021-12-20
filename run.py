from wsgiref import simple_server

from composites.service_api import create_app

# Все что было в 4 задании и
# Добавить сортировку по имени, времени последнего сообщения у пользователей
# Добавить вывод последних Х свежих сообщений

app = create_app()
httpd = simple_server.make_server('0.0.0.0', 1234, app)
httpd.serve_forever()

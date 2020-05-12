from data import db_session
from data.models import User, Detection


db_session.global_init("damn.sqlite")

session = db_session.create_session()

user_1 = User()
user_1.name = "Пользователь 1"
user_1.surname = "11"
user_1.email = "user_1@email.ru"
user_1.set_password('shit')
session.add(user_1)
session.commit()

print('Запрос одного (произвольного) пользователя:')
user = session.query(User).first()
print(user.name)
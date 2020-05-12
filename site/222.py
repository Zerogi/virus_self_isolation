from data import db_session
from data.models import User, Detection


db_session.global_init("try.sqlite")

session = db_session.create_session()


user_1 = User()
user_1.name = "Пользовате§ль 1"
user_1.surname = "11§"
user_1.email = "user_§1@email.ru"
user_1.set_password('s§hit')

damn = Detection()
damn.number_of_people = 10
damn.distance_violation = 2

user_1.detections.append(damn)

session.add(user_1)

session.commit()

print('!')
for i in session.query(User):
    print(i)
    #session.delete(i)

#session.commit()

from data import db_session
from data.models import User, Detection


db_session.global_init("test.sqlite")

session = db_session.create_session()


user_1 = User()
user_1.name = "Пользоватеasdf§ль 1"
user_1.surname = "asdfasdf§"
user_1.email = "user_§1@emasdfasfdail.ru"
user_1.set_password('s§hadfasdfit')

#damn = Detection()
#damn.number_of_people = 10
#damn.distance_violation = 2

#user_1.detections.append(damn)

session.add(user_1)

session.commit()

print('!')
for i in session.query(User):
    #print(i)
    session.delete(i)

session.commit()

for i in session.query(User):
    print(i)

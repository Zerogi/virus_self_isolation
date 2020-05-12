from data import db_session
from data.models import User, Detection

db_session.global_init("try.sqlite")
db_session.create_session()

session = db_session.create_session()

#for i in session.query(User):
 #   session.delete(i)

#ession.commit()
print(1111111111111111111)

for i in session.query(User):
    # session.delete(i)
    print(i.detections[0].number_of_people)

session.commit()
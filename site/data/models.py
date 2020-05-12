import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

# Base = declarative_base()


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # relationship
    detections = relationship("Detection", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Detection(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'detection'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    number_of_people = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    distance_violation = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # relationship
    user_id = sqlalchemy.Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="detections")

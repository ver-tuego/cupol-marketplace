import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin , SerializerMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)

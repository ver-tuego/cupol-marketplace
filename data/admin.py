import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'admin'

    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    gender = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    is_boss = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relationship("User")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from data import db_session
from data.buyer import Buyer
from data.seller import Seller
from data.admin import Admin


class User(SqlAlchemyBase, UserMixin , SerializerMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)

    def get_user(self, db_sess=None):
        if not db_sess:
            db_sess = db_session.create_session()
        return db_sess.query(eval(self.type.capitalize())).get(self.id)

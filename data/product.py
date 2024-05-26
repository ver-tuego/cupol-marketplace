import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'product'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("seller.id"))
    name = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Float)
    quantity = sqlalchemy.Column(sqlalchemy.Integer)
    rating = sqlalchemy.Column(sqlalchemy.Float, default=0.0)
    number_of_purchases = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    seller = orm.relationship("Seller")

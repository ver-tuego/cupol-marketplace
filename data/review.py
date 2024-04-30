import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Review(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'review'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("product.id"))
    buyer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("buyer.id"))
    rating = sqlalchemy.Column(sqlalchemy.Integer)
    text = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    product = orm.relationship("Product")
    buyer = orm.relationship("Buyer")

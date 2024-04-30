import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Basket(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'basket'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    buyer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("buyer.id"))
    product_id = sqlalchemy.Column(sqlalchemy.Integer)
    quantity = sqlalchemy.Column(sqlalchemy.Integer)
    is_bought = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    buyer = orm.relationship("Buyer")

import sqlalchemy
from data.db_session import SqlAlchemyBase


class Emails(SqlAlchemyBase):
    __tablename__ = 'emails'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String)

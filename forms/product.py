from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField('Название товара:', validators=[DataRequired()])
    price = DecimalField('Цена товара:', validators=[DataRequired()])
    quantity = IntegerField('Количество на складе:', validators=[DataRequired()])
    description = TextAreaField('Описание:', validators=[DataRequired()])
    photos = []
    submit = SubmitField('Добавить товар')


class SubmitForm(FlaskForm):
    submit = SubmitField('Добавить товар')

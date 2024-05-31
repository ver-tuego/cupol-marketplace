from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField("Название товара:", validators=[DataRequired()],
                       render_kw={"placeholder": "Название товара"})
    price = DecimalField('Цена товара:', validators=[DataRequired()],
                         render_kw={"placeholder": "Цена товара"})
    quantity = IntegerField('Количество на складе:', validators=[DataRequired()],
                            render_kw={"placeholder": "Количество товара на складе"})
    description = TextAreaField('Описание:', validators=[DataRequired()],
                                render_kw={"placeholder": "Описание товара"})
    submit = SubmitField("Продолжить")


class AddProductForm(FlaskForm):
    submit1 = SubmitField("Добавить товар")


class AddPhotoForm(FlaskForm):
    submit2 = SubmitField("Добавить фото")


class DeletePhotoForm(FlaskForm):
    submit3 = SubmitField("Удалить фото")

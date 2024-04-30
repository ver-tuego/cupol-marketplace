from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, IntegerField, RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    type = RadioField("Зарегистрироваться как:", choices=[("buyer", "Покупатель"), ("seller", "Продавец")],
                      validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    email = EmailField('Почтовый адрес:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль:', validators=[DataRequired()])
    gender = RadioField("Пол:", choices=[("male", "Мужской"), ("female", "Женский")], validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

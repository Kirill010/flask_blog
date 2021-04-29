from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField


class RegisterForm(FlaskForm):
    login = StringField(label='Логин:')
    password = PasswordField(label='Пароль:')
    submit = SubmitField(label='Зарегистрироваться')


class LoginForm(FlaskForm):
    login = StringField(label='Логин:')
    password = PasswordField(label='Пароль:')
    submit = SubmitField(label='Вход')


class PostForm(FlaskForm):
    content = TextAreaField()
    submit = SubmitField(label='Опубликовать')

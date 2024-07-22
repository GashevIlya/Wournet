from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, EmailField
from wtforms.validators import DataRequired, Length, EqualTo
from app.manage import db
from app.main.models import Account, User


def validate_email(form, email):
    user = db.session.query(User).filter_by(email=email.data).first()
    if user:
        raise ValidationError(message='Такой Email есть')


def validate_nickname(form, nickname):
    user = db.session.query(Account).filter_by(nickname=nickname.data.replace(' ', '').lower()).first()
    if user:
        raise ValidationError(message='Такой никнейм есть')


class EntranceForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Length(max=100)])
    password = PasswordField(label='Пароль', validators=[DataRequired(), Length(max=100)])
    remember = BooleanField(label='Запомнить меня')
    submit = SubmitField(label='Войти')


class RegistrationForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Length(min=6, max=100), validate_email])
    nickname = StringField(label='Никнейм', validators=[DataRequired(), Length(min=3, max=15), validate_nickname])
    password = PasswordField(label='Пароль', validators=[DataRequired(), Length(min=8, max=100)])
    repeat_password = PasswordField(label='Повторить пароль', validators=[DataRequired(),
                                                                          EqualTo(fieldname='password',
                                                                                  message='Неверно повторен пароль')])
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Зарегистрироваться')


class ResetPasswordForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Length(max=100)])
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Отправить')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(label='Новый пароль', validators=[DataRequired(), Length(min=8, max=100)])
    repeat_password = PasswordField(label='Повторить новый пароль', validators=[DataRequired(),
                                                                                EqualTo(fieldname='password',
                                                                                        message='Неверно повторен пароль')])
    submit = SubmitField(label='Сохранить')


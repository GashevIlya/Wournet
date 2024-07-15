from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, DateField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from app.manage import db
from app.main.models import Account
from flask_login import current_user


def validate_edit_nickname(form, nickname):
    user = db.session.query(Account).filter_by(nickname=nickname.data).first()
    if user and user.id != current_user.id:
        raise ValidationError(message='Такой никнейм есть')


class EditAccountForm(FlaskForm):
    nickname = StringField(label='Никнейм', validators=[DataRequired(), Length(min=3, max=15), validate_edit_nickname])
    surname = StringField(label='Фамилия', validators=[Length(max=50)])
    name = StringField(label='Имя', validators=[Length(max=50)])
    date_of_birth = DateField(label='Дата рождения', validators=[Optional()])
    gender = RadioField(label='Пол', validators=[DataRequired()],
                        choices=[('man', 'Муж'), ('woman', 'Жен'), ('not_indicated', 'Не указано')])
    city = StringField(label='Город', validators=[Length(max=200)])
    region = StringField(label='Регион/Область', validators=[Length(max=50)])
    country = StringField(label='Страна', validators=[Length(max=50)])
    interests = TextAreaField(label='Интересы', validators=[Length(max=2000)])
    about_me = TextAreaField(label='О себе', validators=[Length(max=2000)])
    submit = SubmitField(label='Изменить')



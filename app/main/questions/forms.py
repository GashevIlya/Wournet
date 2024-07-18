from flask_wtf import FlaskForm, RecaptchaField
from flask_ckeditor import CKEditorField
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length
from bs4 import BeautifulSoup
from app.main.models import Questions
from app.manage import db
from flask_login import current_user


categories = [('IT', 'IT'), ('Машины', 'Машины')]


def validate_description(form, description):
    soup = BeautifulSoup(description.data)
    length_description = len(soup.get_text(strip=True))
    if length_description > 0 and (5 > length_description or length_description > 3000):
        raise ValidationError(message='Длина описания должна быть от 5 до 3000')


def validate_text(form, text):
    soup = BeautifulSoup(text.data)
    length_text = len(soup.get_text(strip=True))
    if 5 > length_text or length_text > 3000:
        raise ValidationError(message='Длина ответа должна быть от 5 до 3000')


def validate_edit_header(form, header):
    if header.data[-1] != '?':
        raise ValidationError(message='Поставте знак вопроса в конец вашего заголовка')
    else:
        question = db.session.query(Questions).filter_by(header=header.data).first()
        if question and question.account_id != current_user.id:
            raise ValidationError(message='Такой заголовок вопроса уже есть')


def validate_create_header(form, header):
    if header.data[-1] != '?':
        raise ValidationError(message='Поставте знак вопроса в конец вашего заголовка')
    else:
        question = db.session.query(Questions).filter_by(header=header.data).first()
        if question:
            raise ValidationError(message='Такой заголовок вопроса уже есть')


class CreateQuestionForm(FlaskForm):
    header = StringField(label='Заголовок', validators=[DataRequired(), Length(min=5, max=50), validate_create_header])
    description = CKEditorField(label='Описание', validators=[validate_description])
    category = SelectField(label='Категория', choices=categories, validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Создать')


class EditQuestionForm(FlaskForm):
    header = StringField(label='Заголовок', validators=[DataRequired(), Length(min=5, max=50), validate_edit_header])
    description = CKEditorField(label='Описание', validators=[validate_description])
    category = SelectField(label='Категория', choices=categories, validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Изменить')


class CreateAnswerForm(FlaskForm):
    answer = CKEditorField(label='Напишите ответ', validators=[DataRequired(), validate_text])
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Создать')


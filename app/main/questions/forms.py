from flask_wtf import FlaskForm, RecaptchaField
from flask_ckeditor import CKEditorField
from wtforms import StringField, BooleanField, SubmitField, SelectMultipleField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length
from bs4 import BeautifulSoup


def validate_description(form, description):
    soup = BeautifulSoup(description.data)
    length_description = len(soup.get_text(strip=True))
    if 5 > length_description or length_description > 3000:
        raise ValidationError(message='Длина описания должна быть от 5 до 3000')


class CreateQuestionForm(FlaskForm):
    header = StringField(label='Заголовок', validators=[DataRequired(), Length(min=5, max=50)])
    description = CKEditorField(label='Описание', validators=[validate_description])
    complexity = SelectField(label='Сложность', choices=[('hard', 'Сложный'), ('normal', 'Средний'),
                                                         ('easy', 'Легкий')], default='normal', validators=[DataRequired()])
    categories = SelectMultipleField(label='Категории', choices=[], validators=[DataRequired()])
    is_draft = BooleanField(label='Добавить в черновик')
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Создать')


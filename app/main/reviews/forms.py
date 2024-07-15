from flask_wtf import FlaskForm, RecaptchaField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreateReviewForm(FlaskForm):
    review = TextAreaField(label='Напишите отзыв об этом проекте или какие-нибудь идеи для его развития',
                           validators=[DataRequired(), Length(min=5, max=2000)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Создать')


class EditReviewForm(FlaskForm):
    review = TextAreaField(label='Напишите отзыв об этом проекте или какие-нибудь идеи для его развития',
                           validators=[DataRequired(), Length(min=5, max=2000)])
    recaptcha = RecaptchaField()
    submit = SubmitField('Изменить')


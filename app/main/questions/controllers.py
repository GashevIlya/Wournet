from app.main.questions.__init__ import questions
from flask_login import login_required
from app.main.questions.forms import CreateQuestionForm
from flask import render_template, request
from app.main.models import Category
from app.manage import db


@questions.route('/question/create', methods=['GET', 'POST'])
@login_required
def create():
    form_create_question = CreateQuestionForm()
    if form_create_question.validate_on_submit():
        pass
    elif request.method == 'GET':
        form_create_question.categories.choices = [(category.id, category.name) for category in db.session.query(Category).all()]
    return render_template('questions/create.html', form_create_question=form_create_question)

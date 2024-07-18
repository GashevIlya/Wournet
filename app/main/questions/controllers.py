from app.main.questions.__init__ import questions
from flask_login import login_required, current_user
from app.main.questions.forms import CreateQuestionForm, EditQuestionForm, CreateAnswerForm
from flask import render_template, flash, redirect, url_for, request
from app.manage import db
from app.main.models import Questions, Answers
from sqlalchemy import func
from enum import Enum


class TypeSortQuestions(str, Enum):
    popular = 'popular'
    unanswered = 'unanswered'
    new = 'new'
    old = 'old'

    def __str__(self):
        return self.name


@questions.route('/question/create', methods=['GET', 'POST'])
@login_required
def create():
    form_create_question = CreateQuestionForm()
    if form_create_question.validate_on_submit():
        try:
            question = Questions(header=form_create_question.header.data, description=form_create_question.description.data,
                                 category=form_create_question.category.data, account_id=current_user.id)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('account.account_user', nickname=current_user.account.nickname))
        except Exception:
            db.session.rollback()
            flash(message='Вопрос не создан')
    return render_template('questions/create.html', form_create_question=form_create_question)


@questions.route('/question/edit/<int:id_question>', methods=['GET', 'POST'])
@login_required
def edit(id_question):
    question = db.session.query(Questions).filter_by(id=id_question, account_id=current_user.id).first_or_404()
    form_edit_question = EditQuestionForm()
    if form_edit_question.validate_on_submit():
        try:
            question.header = form_edit_question.header.data
            question.description = form_edit_question.description.data
            question.category = form_edit_question.category.data
            db.session.merge(question)
            db.session.commit()
            return redirect(url_for('account.account_user', nickname=current_user.account.nickname))
        except Exception:
            db.session.rollback()
            flash(message='Вопрос не отредактировался')
    elif request.method == 'GET':
        form_edit_question.header.data = question.header
        form_edit_question.description.data = question.description
        form_edit_question.category.data = question.category
    return render_template('questions/edit.html', form_edit_question=form_edit_question)


@questions.route('/question/delete/<int:id_question>', methods=['DELETE'])
@login_required
def delete_question(id_question):
    question = db.session.query(Questions).filter_by(id=id_question, account_id=current_user.id).first_or_404()
    try:
        db.session.delete(question)
        db.session.commit()
    except Exception:
        db.session.rollback()
    return ''


@questions.route('/questions/all')
@login_required
def all_questions():
    page = request.args.get('page', type=int, default=1)
    sort = request.args.get('sort', type=TypeSortQuestions, default='popular')
    query = db.session.query(Questions).outerjoin(Answers, Questions.id == Answers.questions_id).group_by(Questions.id)
    if sort == TypeSortQuestions.popular.name:
        sort_questions = query.order_by((func.count(Answers.id) + Questions.views_count).desc())
    elif sort == TypeSortQuestions.unanswered.name:
        sort_questions = query.having(func.count(Answers.id) == 0).order_by(Questions.create_time.desc())
    elif sort == TypeSortQuestions.new.name:
        sort_questions = db.session.query(Questions).order_by(Questions.create_time.desc())
    else:
        sort_questions = db.session.query(Questions).order_by(Questions.create_time.asc())
    questions = sort_questions.paginate(page=page, per_page=15, error_out=False)
    return render_template('questions/all_questions.html', questions=questions, sort=sort)


@questions.route('/questions/<int:id_question>', methods=['GET', 'POST'])
@login_required
def about_question(id_question):
    question = db.session.query(Questions).filter_by(id=id_question).first_or_404()
    form_create_answer = CreateAnswerForm()
    if form_create_answer.validate_on_submit():
        try:
            answer = Answers(text=form_create_answer.answer.data, questions_id=question.id,
                             account_id=current_user.id)
            db.session.add(answer)
            db.session.commit()
            flash(message='Ответ создан', category='success')
        except Exception:
            db.session.rollback()
            flash(message='Ответ не создан', category='danger')
    return render_template('questions/about_question.html', question=question, form_create_answer=form_create_answer)


@questions.route('/questions/<int:id_question>/answers')
@login_required
def answers(id_question):
    page = request.args.get('page', type=int, default=1)
    question = db.session.query(Questions).filter_by(id=id_question).first_or_404()
    all_answers = question.answers.paginate(page=page, per_page=15, error_out=False)
    return render_template('questions/answers.html', all_answers=all_answers, id_question=question.id)


@questions.route('/questions/<int:id_question>/random')
@login_required
def random_questions(id_question):
    question = db.session.query(Questions).filter_by(id=id_question).first_or_404()
    rnd_questions = db.session.query(Questions).filter(Questions.id != question.id).order_by(func.random()).limit(5)
    return render_template('questions/random_questions.html', rnd_questions=rnd_questions)


@questions.route('/answer/delete/<int:id_answer>', methods=['DELETE'])
@login_required
def delete_answer(id_answer):
    answer = db.session.query(Answers).filter_by(id=id_answer, account_id=current_user.id).first_or_404()
    try:
        db.session.delete(answer)
        db.session.commit()
    except Exception:
        db.session.rollback()
    return ''


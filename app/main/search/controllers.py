from app.main.search.__init__ import search
from flask import request, render_template, url_for, redirect
from app.main.models import Questions, Account, Reviews
from app.manage import db
from sqlalchemy import or_
from enum import Enum


class TypeParams(str, Enum):
    questions = 'questions'
    users = 'users'
    reviews = 'reviews'

    def __str__(self):
        return self.name


@search.route('/')
def search_results():
    q = request.args.get('q', type=str)
    page = request.args.get('page', type=int, default=1)
    p = request.args.get('p', type=TypeParams, default='questions')
    if q:
        if p == TypeParams.questions.name:
            query = db.session.query(Questions).filter(or_(Questions.header.contains(q), Questions.description.contains(q)))
        elif p == TypeParams.reviews.name:
            query = db.session.query(Reviews).filter(Reviews.text.contains(q))
        else:
            query = db.session.query(Account).filter(or_(Account.nickname.contains(q), Account.surname.contains(q),
                                                         Account.name.contains(q)))
        query = query.paginate(page=page, per_page=15, error_out=True)
        return render_template('search/search_results.html', q=q, query=query, p=p)
    return redirect(url_for('questions.all_questions'))


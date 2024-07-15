from flask import render_template, request
from flask_login import login_required
from app.main.models import Account, Reviews, Answers, Questions
from app.manage import db
from sqlalchemy import func
from app.main.users.__init__ import users


@users.route('/all')
@login_required
def all_users():
    page = request.args.get('page', type=int, default=1)
    users = db.session.query(Account).outerjoin(Reviews, Account.id == Reviews.account_id).\
        outerjoin(Questions, Account.id == Questions.account_id).outerjoin(Answers, Account.id == Answers.id).\
        group_by(Account.id).order_by((func.count(Reviews.id) + func.count(Questions.id) + func.count(Answers.id)).desc()).\
        paginate(page=page, per_page=15, error_out=True)
    return render_template('users/all_users.html', users=users)


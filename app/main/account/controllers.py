from flask import render_template, request, flash
from flask_login import login_required, current_user
from pycbrf.toolbox import ExchangeRates
import arrow
from app.manage import cg, db, cache
from app.main.models import Account, Reviews, Questions
from app.main.account.forms import EditAccountForm
from app.main.account.__init__ import account


@account.route('/<string:nickname>')
@login_required
def account_user(nickname):
    user = db.session.query(Account).filter_by(nickname=nickname).first_or_404()
    return render_template('account/account.html', user=user)


@account.route('/<string:nickname>/data')
@login_required
def data(nickname):
    user = db.session.query(Account).filter_by(nickname=nickname).first_or_404()
    return render_template('account/data.html', user=user)


@account.route('/<string:nickname>/questions')
@login_required
def questions(nickname):
    user = db.session.query(Account).filter_by(nickname=nickname).first_or_404()
    page = request.args.get('page', type=int, default=1)
    questions_user = user.questions.order_by(Questions.create_time.desc()).\
        paginate(page=page, per_page=15, error_out=False)
    return render_template('account/questions.html', questions_user=questions_user, user=user)


@account.route('/<string:nickname>/reviews')
@login_required
def reviews(nickname):
    page = request.args.get('page', type=int, default=1)
    user = db.session.query(Account).filter_by(nickname=nickname).first_or_404()
    reviews_user = user.reviews.order_by(Reviews.create_time.desc()).\
        paginate(page=page, per_page=15, error_out=False)
    return render_template('account/reviews.html', reviews_user=reviews_user, user=user)


@account.route('/<string:nickname>/information')
@login_required
def information(nickname):
    user = db.session.query(Account).filter_by(nickname=nickname).first_or_404()
    return render_template('account/information.html', user=user)


@account.route('/currency/rate')
@login_required
@cache.cached(timeout=3600)
def currency_rate():
    rates = ExchangeRates(str(arrow.now('Europe/Moscow').date()))
    return render_template('account/currency_rate.html', currency_dollar=rates['USD'].value,
                           currency_euro=rates['EUR'].value)


@account.route('/cryptocurrency/rate')
@login_required
@cache.cached(timeout=3600)
def cryptocurrency_rate():
    cryptocurrency_bitcoin = cg.get_price(ids='bitcoin', vs_currencies='rub')
    cryptocurrency_ton = cg.get_price(ids='the-open-network', vs_currencies='rub')
    return render_template('account/cryptocurrency_rate.html',
                           cryptocurrency_bitcoin=cryptocurrency_bitcoin['bitcoin']['rub'],
                           cryptocurrency_ton=cryptocurrency_ton['the-open-network']['rub'])


@account.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form_edit_account = EditAccountForm()
    user = current_user.account
    if form_edit_account.validate_on_submit():
        try:
            user.nickname = form_edit_account.nickname.data
            user.surname = form_edit_account.surname.data
            user.name = form_edit_account.name.data
            user.date_of_birth = form_edit_account.date_of_birth.data
            user.gender.name = form_edit_account.gender.data
            user.location.city = form_edit_account.city.data
            user.location.region = form_edit_account.region.data
            user.location.country = form_edit_account.country.data
            user.interests = form_edit_account.interests.data
            user.about_me = form_edit_account.about_me.data
            db.session.merge(user)
            db.session.commit()
            flash(message='Данные изменены', category='success')
        except Exception:
            db.session.rollback()
            flash(message='Данные не изменены', category='danger')
    elif request.method == 'GET':
        form_edit_account.gender.data = user.gender.name
        form_edit_account.interests.data = user.interests if user.interests else ''
        form_edit_account.about_me.data = user.about_me if user.about_me else ''
    return render_template('account/edit.html', form_edit_account=form_edit_account)


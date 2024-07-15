from flask import render_template, flash, request
from flask_login import login_required, current_user
from app.main.reviews.forms import CreateReviewForm, EditReviewForm
from app.manage import db
from app.main.models import Reviews
from app.main.reviews.__init__ import reviews


@reviews.route('/review/create', methods=['GET', 'POST'])
@login_required
def create():
    form_create_review = CreateReviewForm()
    if form_create_review.validate_on_submit():
        try:
            review = Reviews(text=form_create_review.review.data, account_id=current_user.id)
            db.session.add(review)
            db.session.commit()
            flash(message='Отзыв создан', category='success')
        except Exception:
            db.session.rollback()
            flash(message='Отзыв не создан', category='danger')
    return render_template('reviews/create.html', form_create_review=form_create_review)


@reviews.route('/reviews/all')
@login_required
def all_reviews():
    page = request.args.get('page', type=int, default=1)
    reviews_users = db.session.query(Reviews).order_by(Reviews.create_time.desc()).\
        paginate(page=page, per_page=15, error_out=True)
    return render_template('reviews/all_reviews.html', reviews_users=reviews_users)


@reviews.route('/review/delete/<int:id_review>', methods=['DELETE'])
@login_required
def delete_review(id_review):
    review = Reviews.query.filter_by(id=id_review, account_id=current_user.id).first_or_404()
    try:
        db.session.delete(review)
        db.session.commit()
    except Exception:
        pass
    return ''


@reviews.route('/review/edit/<int:id_review>', methods=['GET', 'POST'])
@login_required
def edit(id_review):
    review = Reviews.query.filter_by(id=id_review, account_id=current_user.id).first_or_404()
    form_edit_review = EditReviewForm()
    if form_edit_review.validate_on_submit():
        try:
            review.text = form_edit_review.review.data
            db.session.merge(review)
            db.session.commit()
            flash(message='Отзыв отредактировался', category='success')
        except Exception:
            db.session.rollback()
            flash(message='Отзыв не отредактировался', category='danger')
    elif request.method == 'GET':
        form_edit_review.review.data = review.text
    return render_template('reviews/edit.html', form_edit_review=form_edit_review)


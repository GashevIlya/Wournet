from app.manage import app, login_manager, db, mail
from flask import render_template, redirect, url_for, flash
from app.main.models import Account, Role, User, Gender, Location
from flask_login import logout_user, login_required, login_user, current_user
from app.main.auth.forms import EntranceForm, RegistrationForm, ResetPasswordForm, ChangePasswordForm
from flask_bcrypt import check_password_hash, generate_password_hash
from functools import wraps
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.main.auth.__init__ import auth
from threading import Thread


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, exception=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=exception
        )
    except Exception:
        return False
    return email


def create_user(email, password, nickname, role='user'):
    user = User(email=email, password=generate_password_hash(password).decode('utf8'))
    db.session.add(user)
    db.session.flush()
    role_user = Role(id=user.id, name=role)
    account_user = Account(id=user.id, nickname=nickname)
    gender_user = Gender(id=user.id)
    location_user = Location(id=user.id)
    db.session.add_all([role_user, account_user, gender_user, location_user])
    db.session.commit()


def check_authenticated_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('account.account_user', nickname=current_user.account.nickname))
        return func(*args, **kwargs)
    return wrapper


@app.route('/', methods=['GET', 'POST'])
@auth.route('/entrance', methods=['GET', 'POST'])
@check_authenticated_user
def entrance():
    form_entrance = EntranceForm()
    if form_entrance.validate_on_submit():
        user = db.session.query(User).filter_by(email=form_entrance.email.data).first()
        if user and check_password_hash(user.password, form_entrance.password.data):
            login_user(user, remember=form_entrance.remember.data)
            return redirect(url_for('account.account_user', nickname=user.account.nickname))
        flash(message='Неверный Email или пароль')
    return render_template('auth/entrance.html', form_entrance=form_entrance)


@auth.route('/registration', methods=['GET', 'POST'])
@check_authenticated_user
def registration():
    form_registration = RegistrationForm()
    if form_registration.validate_on_submit():
        try:
            create_user(email=form_registration.email.data, password=form_registration.password.data,
                        nickname=form_registration.nickname.data.replace(' ', '').lower())
            return redirect(url_for('auth.entrance'))
        except Exception:
            db.session.rollback()
            flash(message='Данные не сохранились')
    return render_template('auth/registration.html', form_registration=form_registration)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.entrance'))


def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(email, token):
    subject = 'Восстановление аккаунта'
    body = f'<p>Здравствуйте,</p><p>Мы получили запрос на сброс пароля для вашего аккаунта. ' \
           'Если вы не запрашивали сброс пароля, пожалуйста, проигнорируйте это сообщение.</p>' \
           f'<p>Для сброса пароля пройдите по ссылке ниже:</p><p>https://wournet.onrender.com/auth/change/password/{token}</p>' \
           '<p>Если ссылка не работает, скопируйте и вставьте ее в адресную строку браузера.</p>' \
           '<p>С уважением, Команда поддержки.</p>'
    msg = Message(subject, recipients=[email])
    msg.html = body
    Thread(target=send_async_email, args=(msg, )).start()


@auth.route('/reset/password', methods=['GET', 'POST'])
@check_authenticated_user
def reset_password():
    form_reset_password = ResetPasswordForm()
    if form_reset_password.validate_on_submit():
        user = db.session.query(User).filter_by(email=form_reset_password.email.data).first()
        if user:
            try:
                user.is_reset_password = True
                db.session.commit()
                token = generate_token(email=user.email)
                send_email(email=user.email, token=token)
                flash(message='Письмо отправлено', category='success')
            except Exception:
                db.session.rollback()
                flash(message='Письмо не отправлено', category='danger')
        else:
            flash(message='Такого Email нет', category='danger')
    return render_template('auth/reset_password.html', form_reset_password=form_reset_password)


@auth.route('/change/password/<token>', methods=['GET', 'POST'])
@check_authenticated_user
def change_password(token):
    email = confirm_token(token=token)
    if email is not False:
        user = db.session.query(User).filter_by(email=email).first()
        if user.is_reset_password is True:
            form_change_password = ChangePasswordForm()
            if form_change_password.validate_on_submit():
                hash_password = generate_password_hash(form_change_password.password.data).decode('utf8')
                try:
                    user.password = hash_password
                    user.is_reset_password = False
                    db.session.commit()
                    return redirect(url_for('auth.entrance'))
                except Exception:
                    db.session.rollback()
                    flash(message='Пароль не изменен')
            return render_template('auth/change_password.html', form_change_password=form_change_password)
    return redirect(url_for('auth.entrance'))


@auth.route('/privacy/policy')
@check_authenticated_user
def privacy_policy():
    return render_template('auth/privacy_policy.html')


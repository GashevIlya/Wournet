from app.manage import db
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, ENUM, TIMESTAMP, BOOLEAN, DATE
import arrow
from flask_login import UserMixin
import hashlib


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(INTEGER, primary_key=True)
    email = db.Column(VARCHAR, nullable=False, unique=True)
    is_reset_password = db.Column(BOOLEAN, nullable=False, default=False)
    password = db.Column(VARCHAR, nullable=False)
    account = db.relationship('Account', backref=db.backref('user'), uselist=False)
    role = db.relationship('Role', backref=db.backref('user'), uselist=False)

    def hash_email(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def __repr__(self):
        return f'{self.id}'


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(INTEGER, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(ENUM('admin', 'user', name='role_user'), nullable=False, default='user')

    def __repr__(self):
        return f'{self.id}'


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(INTEGER, db.ForeignKey('user.id'), primary_key=True)
    nickname = db.Column(VARCHAR, nullable=False, unique=True)
    surname = db.Column(VARCHAR)
    name = db.Column(VARCHAR)
    date_of_birth = db.Column(DATE)
    interests = db.Column(VARCHAR)
    about_me = db.Column(VARCHAR(2000))
    registered = db.Column(DATE, nullable=False, default=arrow.now('Europe/Moscow').date())
    location = db.relationship('Location', backref=db.backref('account'), uselist=False)
    gender = db.relationship('Gender', backref=db.backref('account'), uselist=False)
    reviews = db.relationship('Reviews', backref=db.backref('account'), lazy='dynamic')
    questions = db.relationship('Questions', backref=db.backref('account'), lazy='dynamic')
    answers = db.relationship('Answers', backref=db.backref('account'), lazy='dynamic')

    def format_date_of_birth(self):
        return arrow.get(self.date_of_birth).format('DD MMM YYYY года', locale='ru')

    def format_registered(self):
        return arrow.get(self.registered).format('DD MMM YYYY года', locale='ru')

    def count_reviews(self):
        return self.reviews.count()

    def count_questions(self):
        return self.questions.count()

    def count_score(self):
        return self.answers.count() * 10

    def __repr__(self):
        return f'{self.id}'


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(INTEGER, db.ForeignKey('account.id'), primary_key=True)
    name = db.Column(ENUM('man', 'woman', 'not_indicated', name='gender_user'), default='not_indicated')

    def __repr__(self):
        return f'{self.id}'


class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(INTEGER, db.ForeignKey('account.id'), primary_key=True)
    city = db.Column(VARCHAR)
    region = db.Column(VARCHAR)
    country = db.Column(VARCHAR)

    def __repr__(self):
        return f'{self.id}'


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(INTEGER, primary_key=True)
    text = db.Column(VARCHAR, nullable=False)
    create_time = db.Column(TIMESTAMP, nullable=False, default=arrow.now('Europe/Moscow').datetime)
    account_id = db.Column(INTEGER, db.ForeignKey('account.id'))

    def format_create_time(self):
        return arrow.get(self.create_time).format('DD MMM YYYY.г в H:mm', locale='ru')

    def __repr__(self):
        return f'{self.id}'


class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(INTEGER, primary_key=True)
    header = db.Column(VARCHAR, nullable=False, unique=True)
    description = db.Column(VARCHAR, nullable=True)
    create_time = db.Column(TIMESTAMP, nullable=False, default=arrow.now('Europe/Moscow').datetime)
    views_count = db.Column(INTEGER, nullable=False, default=0)
    category = db.Column(VARCHAR, nullable=False)
    account_id = db.Column(INTEGER, db.ForeignKey('account.id'))
    answers = db.relationship('Answers', backref=db.backref('questions'), cascade='all, delete', lazy='dynamic')

    def format_create_time(self):
        return arrow.get(self.create_time).format('DD MMM YYYY.г в H:mm', locale='ru')

    def format_views_count(self):
        if self.views_count < 1000:
            return self.views_count
        elif 1000 <= self.views_count < 10000:
            return f'{str(self.views_count)[0]}.{str(self.views_count)[1]} тыс'
        elif 10000 <= self.views_count < 100000:
            return f'{str(self.views_count)[:2]}.{str(self.views_count)[2]} тыс'
        elif 100000 <= self.views_count < 1000000:
            return f'{str(self.views_count)[:3]}.{str(self.views_count)[3]} тыс'
        elif 1000000 <= self.views_count < 10000000:
            return f'{str(self.views_count)[0]}.{str(self.views_count)[1]} млн'
        elif 10000000 <= self.views_count < 100000000:
            return f'{str(self.views_count)[:2]}.{str(self.views_count)[2]} млн'
        elif 100000000 <= self.views_count < 1000000000:
            return f'{str(self.views_count)[:3]}.{str(self.views_count)[3]} млн'
        else:
            return f'{str(self.views_count)[0]}.{str(self.views_count)[1]} млрд'

    def count_answers(self):
        return self.answers.count()

    def __repr__(self):
        return f'{self.id}'


class Answers(db.Model):
    __tablename__ = 'answers'

    id = db.Column(INTEGER, primary_key=True)
    text = db.Column(VARCHAR, nullable=False)
    create_time = db.Column(TIMESTAMP, nullable=False, default=arrow.now('Europe/Moscow').datetime)
    questions_id = db.Column(INTEGER, db.ForeignKey('questions.id'))
    account_id = db.Column(INTEGER, db.ForeignKey('account.id'))

    def format_create_time(self):
        return arrow.get(self.create_time).format('DD MMM YYYY.г в H:mm', locale='ru')

    def __repr__(self):
        return f'{self.id}'


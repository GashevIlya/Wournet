from app.manage import db, app
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, ENUM, DATETIME, BOOLEAN, DATE
import arrow
from flask_login import UserMixin
import hashlib


category_questions = db.Table(
    'category_questions',
    db.Column('questions_id', INTEGER, db.ForeignKey('questions.id')),
    db.Column('category_id', INTEGER, db.ForeignKey('category.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(INTEGER, primary_key=True)
    gmail = db.Column(VARCHAR(100), nullable=False, unique=True)
    is_reset_password = db.Column(BOOLEAN, nullable=False, default=False)
    password = db.Column(VARCHAR(100), nullable=False)
    account = db.relationship('Account', backref=db.backref('user'), uselist=False)
    role = db.relationship('Role', backref=db.backref('user'), uselist=False)

    def hash_gmail(self):
        return hashlib.md5(self.gmail.lower().encode('utf-8')).hexdigest()

    def __repr__(self):
        return f'{self.id}'


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(INTEGER, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(ENUM('admin', 'user'), nullable=False, default='user')

    def __repr__(self):
        return f'{self.id}'


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(INTEGER, db.ForeignKey('user.id'), primary_key=True)
    nickname = db.Column(VARCHAR(15), nullable=False, unique=True)
    surname = db.Column(VARCHAR(50))
    name = db.Column(VARCHAR(50))
    date_of_birth = db.Column(DATE)
    interests = db.Column(VARCHAR(2000))
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
        return self.answers.count()

    def __repr__(self):
        return f'{self.id}'


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(INTEGER, db.ForeignKey('account.id'), primary_key=True)
    name = db.Column(ENUM('man', 'woman', 'not_indicated'), default='not_indicated')

    def __repr__(self):
        return f'{self.id}'


class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column(INTEGER, db.ForeignKey('account.id'), primary_key=True)
    city = db.Column(VARCHAR(200))
    region = db.Column(VARCHAR(50))
    country = db.Column(VARCHAR(50))

    def __repr__(self):
        return f'{self.id}'


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(INTEGER, primary_key=True)
    text = db.Column(VARCHAR(2000), nullable=False)
    create_time = db.Column(DATETIME, nullable=False, default=arrow.now('Europe/Moscow').datetime)
    account_id = db.Column(INTEGER, db.ForeignKey('account.id'))

    def format_create_time(self):
        return arrow.get(self.create_time).format('DD MMM YYYY.г в H:mm', locale='ru')

    def __repr__(self):
        return f'{self.id}'


class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(INTEGER, primary_key=True)
    header = db.Column(VARCHAR(50), nullable=False, unique=True)
    description = db.Column(VARCHAR(5000), nullable=True)
    create_time = db.Column(DATETIME, nullable=False, default=arrow.now('Europe/Moscow').datetime)
    views_count = db.Column(INTEGER, nullable=False, default=0)
    complexity = db.Column(ENUM('hard', 'normal', 'easy'), nullable=False)
    is_draft = db.Column(BOOLEAN, nullable=False, default=False)
    account_id = db.Column(INTEGER, db.ForeignKey('account.id'))
    category = db.relationship('Category', secondary=category_questions, backref=db.backref('questions'),
                               lazy='dynamic', cascade='all, delete')
    answers = db.relationship('Answers', backref=db.backref('questions'), cascade='all, delete', lazy='dynamic')

    def __repr__(self):
        return f'{self.id}'


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR(50), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.id}'


class Answers(db.Model):
    __tablename__ = 'answers'

    id = db.Column(INTEGER, primary_key=True)
    text = db.Column(VARCHAR(5000), nullable=False)
    create_time = db.Column(DATETIME, nullable=False, default=arrow.now('Europe/Moscow').datetime)
    questions_id = db.Column(INTEGER, db.ForeignKey('questions.id'))
    account_id = db.Column(INTEGER, db.ForeignKey('account.id'))

    def __repr__(self):
        return f'{self.id}'


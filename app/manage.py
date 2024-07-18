from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_avatars import Avatars
from flask_mail import Mail
from pycoingecko import CoinGeckoAPI
from flask_ckeditor import CKEditor
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
from flask_sslify import SSLify


app = Flask(__name__)

app.config.from_object('app.config.Config')


class MyAdminINdexView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'admin':
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.entrance'))


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.entrance'
login_manager.login_message = 'Войдите в систему'
bcrypt = Bcrypt(app)
avatars = Avatars(app)
mail = Mail(app)
cg = CoinGeckoAPI()
ckeditor = CKEditor(app)
admin = Admin(app, name='Админка', template_mode='bootstrap4', index_view=MyAdminINdexView())
cache = Cache(app)
limiter = Limiter(get_remote_address, app=app, default_limits=['2 per second'], strategy="fixed-window")
celery = Celery('tasks', broker=app.config['REDIS_BROKER'], include='app.main.auth.__init__')
sslify = SSLify(app)


from app.main.admin import *
from app.main.errors import *
from app.main.auth.__init__ import auth
from app.main.account.__init__ import account
from app.main.reviews.__init__ import reviews
from app.main.users.__init__ import users
from app.main.questions.__init__ import questions
from app.main.search.__init__ import search


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(reviews)
app.register_blueprint(questions)
app.register_blueprint(search, url_prefix='/search')


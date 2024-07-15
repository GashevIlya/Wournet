from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_avatars import Avatars
from flask_mail import Mail
from pycoingecko import CoinGeckoAPI
from flask_ckeditor import CKEditor


app = Flask(__name__)

app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.entrance'
login_manager.login_message = 'Войдите в систему'
bcrypt = Bcrypt(app)
avatars = Avatars(app)
mail = Mail(app)
cg = CoinGeckoAPI()
ckeditor = CKEditor(app)


from app.main.auth.__init__ import auth
from app.main.account.__init__ import account
from app.main.reviews.__init__ import reviews
from app.main.users.__init__ import users
from app.main.questions.__init__ import questions


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(reviews)
app.register_blueprint(questions)


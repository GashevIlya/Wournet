from app.main.models import *
from flask_admin.contrib.sqla import ModelView
from app.manage import admin, db
from flask_login import current_user
from flask import redirect, url_for


class MyModelView(ModelView):
    can_create = False

    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'admin':
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.entrance'))


class MainModel(MyModelView):
    can_delete = False
    column_display_pk = True


admin.add_view(MainModel(User, db.session))
admin.add_view(MainModel(Role, db.session))
admin.add_view(MainModel(Account, db.session, endpoint='account_'))
admin.add_view(MainModel(Gender, db.session))
admin.add_view(MainModel(Location, db.session))
admin.add_view(MyModelView(Reviews, db.session, endpoint='reviews_'))
admin.add_view(MyModelView(Questions, db.session, endpoint='questions_'))
admin.add_view(MyModelView(Answers, db.session))

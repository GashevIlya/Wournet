from app.main.models import *
from flask_admin.contrib.sqla import ModelView
from app.manage import admin, db
from flask_login import current_user
from flask import redirect, url_for


class BaseModelView(ModelView):
    can_create = False

    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'admin':
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.entrance'))


class MainModelView(BaseModelView):
    can_delete = False


class UserModel(MainModelView):
    column_display_pk = True


class RoleModel(MainModelView):
    column_list = ('id', 'name')


admin.add_view(UserModel(User, db.session))
admin.add_view(RoleModel(Role, db.session))
admin.add_view(MainModelView(Account, db.session, endpoint='account_'))
admin.add_view(MainModelView(Gender, db.session))
admin.add_view(MainModelView(Location, db.session))
admin.add_view(BaseModelView(Reviews, db.session, endpoint='reviews_'))
admin.add_view(BaseModelView(Questions, db.session, endpoint='questions_'))
admin.add_view(BaseModelView(Answers, db.session))

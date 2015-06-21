from flask.ext.admin import BaseView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

class MyBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.admin

class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.admin

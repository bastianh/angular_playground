from flask.ext.admin import AdminIndexView, Admin, expose
from backend.models.user import User
from backend.modules.admin import MyBaseView
from backend.modules.admin.models import UserView, ApiCallView
from backend.signals import on_init_app
from backend.utils.database import db
from backend.utils.eveapi import ApiCall


class MyView(MyBaseView):
    @expose('/')
    def index(self):
        return self.render("admin/index.html", data="hello")

class MyHomeView(AdminIndexView, MyBaseView):
    @expose()
    def index(self):
        return self.render("admin/index.html", data=self._template)

@on_init_app.connect
def init_app(app):
    admin = Admin(index_view=MyHomeView(), template_mode='bootstrap2')
    admin.init_app(app)
    admin.add_view(MyView(name='Hello'))
    admin.add_view(UserView(User, db.session, category="Models"))
    admin.add_view(ApiCallView(ApiCall, db.session, category="Models"))


import xmlrpc.client

from flask import request, abort, redirect, url_for
from flask.ext.admin import BaseView, expose

from maintain.signals import get_admin_modules


@get_admin_modules.connect
def init_app(app):
    return Supervisor(name='Supervisor'), 100


class Supervisor(BaseView):
    def is_accessible(self):
        return True

    @property
    def proxy(self):
        return xmlrpc.client.ServerProxy("http://localhost:9001/RPC2")

    @expose('/')
    def index(self):
        data = self.proxy.supervisor.getAllProcessInfo()
        return self.render("maintain/supervisor.html", data=data)

    @expose('/status')
    def change_status(self):
        name = request.args.get("name")
        new_status = request.args.get("status", 0, int)
        if not name or not new_status:
            abort(400)
        if new_status == 1:
            self.proxy.supervisor.startProcess(name)
        elif new_status == -1:
            self.proxy.supervisor.stopProcess(name)

        return redirect(url_for(".index"))
        return "%s %s" % (1, request.args)

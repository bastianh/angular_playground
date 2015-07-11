import os

from flask import current_app, flash
from flask.ext.admin import expose, AdminIndexView
from itsdangerous import TimestampSigner
from wtforms import Form, StringField, validators

from backend import settings
from backend.utils.config import INIConfig

class MTLogin(Form):
    code = StringField(u'Login Code', validators=[validators.input_required()])

class HomeView(AdminIndexView):
    @expose('/', methods=["GET","POST"])
    def index(self):
        secret_key = current_app.config.get("SECRET_KEY")
        if current_app.config.get("TEMP_SECRET_KEY"):
            inifile = INIConfig()
            inifile.read(settings.CONFIG_FILE)
            if not inifile.has_section("flask"):
                inifile.add_section("flask")
            flask_config = inifile["flask"]
            if not flask_config.get("SECRET_KEY"):
                flash("Missing SECRET_KEY, creating a new config file...", "error")
                inifile.set("flask", "SECRET_KEY", str(os.urandom(24)))
                with open(settings.CONFIG_FILE, 'w') as configfile:
                    inifile.write(configfile)
            else:
                flash("A new SECRET_KEY is in the configfile, but app still needs a restart...", "warning")

        s = TimestampSigner(secret_key)
        print(78 * "=" + "\nLogin Code: %s\n" % s.sign('maintain').decode("utf-8") + 78 * "=")
        form = MTLogin()
        return self.render('home/index.html', form=form)

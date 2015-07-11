from flask import current_app
from flask.ext.admin import BaseView


class MaintainBaseView(BaseView):
    def is_accessible(self):
        if current_app.config.get("TEMP_SECRET_KEY"):
            return False
        return True


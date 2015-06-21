from flask import flash
from backend.modules.admin import BaseModelView


class UserView(BaseModelView):
    can_create = False
    can_delete = False

    form_columns  = ['email', 'admin']

    column_list = ('character_name', 'corp_name', 'alliance_name', 'admin', 'last_login')

    column_searchable_list = ('character_name', 'corp_name', 'alliance_name')

    column_filters = ('character_name', 'corp_name', 'alliance_name')


class ApiCallView(BaseModelView):
    can_create = False
    can_delete = False
    can_edit = True

    # column_editable_list = ('success',)

    column_display_pk = True
    column_default_sort = ('id', True)
    column_list = ('id','created', 'path', 'params', 'success')

    def update_model(self, form, model):
        flash('Einträge in dieser Tabelle können nicht geändert werden.', 'error')
        return False

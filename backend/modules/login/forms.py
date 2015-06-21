import logging

from evelink.eve import EVE
from wtforms import validators, Form, TextField, ValidationError

from backend.utils.eveapi import EVEAPI

logger = logging.getLogger(__name__)


class DebugLoginForm(Form):
    character_id = None
    character_name = None
    corp_id = None
    corp_name = None
    alliance_id = None
    alliance_name = None
    character = TextField('Character', [validators.Required()])

    def validate_character(form, field):
        api = EVE(api=EVEAPI.cached())
        form.character_id = api.character_id_from_name(field.data).result
        if not form.character_id:
            raise ValidationError('Character nicht gefunden!')

        data = api.character_info_from_id(form.character_id).result
        form.character_name = data.get("name")
        corp = data.get("corp", {})
        form.corp_id = corp.get("id")
        form.corp_name = corp.get("name")
        alliance = data.get("alliance", {})
        form.alliance_id = alliance.get("id")
        form.alliance_name = alliance.get("name")

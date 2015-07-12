import ast
from configparser import SafeConfigParser

from flask import current_app


class INIConfig(SafeConfigParser):

    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.optionxform = str
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.from_inifile = self.from_inifile

    def from_inifile(self, path, app=None, config=None):
        print("XXXX %r", config)
        if app:
            config = app.config
        if not config:
            config = current_app.config
        self.read(path)
        for section in self.sections():
            options = self.options(section)
            for option in options:
                parsed_value = self.parse_value(section, option)
                if section == 'flask':
                    config[option.upper()] = parsed_value
                else:
                    config.setdefault(section, {})[option] = parsed_value

    def parse_value(self, section, option):
        for method in [self.getint, self.getfloat, self.getboolean]:
            try:
                return method(section, option)
            except ValueError:
                pass

        value = self.get(section, option).strip()
        try:
            # maybe its a dict, list or tuple
            if value and value[0] in [ '[', '{', '(' ]:
                return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass

        return value

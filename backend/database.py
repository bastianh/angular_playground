from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import event
from backend.signals import on_init_app
from backend.utils.dogpile_cache import rediscache
from marshmallow_sqlalchemy import ModelSchema, SchemaOpts
from flask import abort

db = SQLAlchemy()
Base = declarative_base()

@on_init_app.connect
def init_app(app):
    db.init_app(app)


class BaseOpts(SchemaOpts):
    def __init__(self, meta):
        if not hasattr(meta, 'sql_session'):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta)

class BaseSchema(ModelSchema):
    OPTIONS_CLASS = BaseOpts

class CRUDMixin(object):
    @classmethod
    def get_by_id(cls, id):
        if not id:
            return
        return db.session.query(cls).get(id)

    @classmethod
    def get_or_404(cls, id):
        if not id:
            abort(404)
        obj = db.session.query(cls).get(id)
        if not obj:
            abort(404)
        return obj

    @classmethod
    def get_or_create(cls,commit=True, create_method_kwargs=None, **kwargs):
        try:
            return db.session.query(cls).filter_by(**kwargs).one()
        except NoResultFound:
            kwargs.update(create_method_kwargs or {})
            return cls.create(commit, **kwargs)

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        db.session.flush()
        return commit and instance.save() or instance

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class CRUDMixinCached(CRUDMixin):
    @classmethod
    def get_by_id(cls, id, max_age=900):
        """ returns the object ... maximum object age (cache_time) time default 900 """
        if not id:
            return None
        if cls.__mapper__.primary_key[0].type == int:
            id = int(id)
        # zuerst in der aktuellen session nachgucken ob es nicht schon da ist
        for obcls, obid in db.session.identity_map:
            if obcls == cls and obid[0] == id:
                obj = db.session.identity_map[(obcls, obid)]
                return obj
        cachekey = "CRUDCACHE:%s_%s" % (cls.__name__, str(id))
        obj = rediscache.get(cachekey, expiration_time=max_age)
        if not obj:
            obj = super(CRUDMixinCached, cls).get_by_id(id)
            if obj:
                rediscache.set(cachekey, obj)
                # logger.debug("CRUDMixinCached %r:get_by_id(%r) LOADED %r", cls.__name__, id, obj)
        else:
            db.session.add(obj)
        return obj

    def flush_cache(self):
        # logger.debug("CRUDMixinCached %r:_flush_cache() BUSTED: %r", self.__class__.__name__, self)
        keyid = self.__getattribute__(self.__class__.__mapper__.primary_key[0].name)
        if keyid:  # evtl ist das objekt noch gar nicht gespeichert
            cachekey = "CRUDCACHE:%s_%s" % ( self.__class__.__name__, keyid)
            rediscache.delete(cachekey)

    @staticmethod
    def _flush_event(mapper, connection, target):
        """
        Called on object modification to flush cache of dependencies
        """
        target.flush_cache()

    @classmethod
    def __declare_last__(cls):
        """
        Auto clean the caches, including listings possibly associated with
        this instance, on delete, update and insert.
        """
        event.listen(cls, 'before_delete', cls._flush_event)
        event.listen(cls, 'before_update', cls._flush_event)
        event.listen(cls, 'before_insert', cls._flush_event)

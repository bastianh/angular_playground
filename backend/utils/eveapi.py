from datetime import datetime, timedelta
import pickle
import time
import collections

import evelink
import requests
import sqlalchemy as sa

from sqlalchemy.dialects import postgres

from backend.signals import on_init_app
from backend.utils.database import db, Base
from backend.utils.redis_ext import redis

APIResultEx = collections.namedtuple("APIResultEx", [
    "result",
    "timestamp",
    "expires",
    "apicallid"
])


@on_init_app.connect
def init_app(app):
    evelink.api.default_cache = RedisCache(redis)


class ApiCall(Base):
    __tablename__ = "app_api_calls"

    ACCOUNT_APIKEYINFO = "account/APIKeyInfo"
    CORP_ASSETLIST = "corp/AssetList"
    CORP_LOCATIONS = "corp/Locations"
    CORP_MEMBERSECURITY = "corp/MemberSecurity"
    CORP_MEMBERTRACKING = "corp/MemberTracking"
    CORP_BLUEPRINTS = "corp/Blueprints"
    CORP_INDUSTRYJOBS = "corp/IndustryJobs"
    CORP_INDUSTRYJOBS_HISTORY = "corp/IndustryJobsHistory"
    CORP_MARKETORDERS = "corp/MarketOrders"
    CORP_WALLETTRANSACTIONS = "corp/WalletTransactions"
    CORP_WALLETJOURNAL = "corp/WalletJournal"

    id = sa.Column(sa.BigInteger, sa.Sequence('app_api_calls_id_seq'), primary_key=True)
    created = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False,
                        server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), index=True)

    path = sa.Column(sa.String, nullable=False, index=True)
    params = sa.Column(postgres.JSON)

    success = sa.Column(sa.Boolean, default=False, server_default='0', nullable=False, index=True)

    result_timestamp = sa.Column(sa.DateTime)
    result_expires = sa.Column(sa.DateTime)

    apikey_id = sa.Column(sa.Integer)
    api_error_code = sa.Column(sa.Integer)
    api_error_message = sa.Column(sa.String)

    http_error_code = sa.Column(sa.Integer)
    http_error_message = sa.Column(sa.String)

    @classmethod
    def get_last_call(cls, path, apikey_id=None, success_only=True, **kwargs):
        """
                über k(ey)w(ord)args können parameter aus dem params getestet werde (gecastet auf string)
        """
        c = cls.__table__.c
        s = sa.select([c.id, c.created, c.result_timestamp, c.result_expires, c.success]).where(c.path == path)
        if success_only:
            s = s.where(c.success.is_(True))

        if apikey_id:
            s = s.where(c.apikey_id == apikey_id)

        for k, v in kwargs.items():
            s = s.where(c.params[k].astext == str(v))

        s = s.order_by(c.id.desc()).limit(1)
        result = db.engine.execute(s).first()
        return result

    @classmethod
    def check_expired(cls, path, min_age=None, error_wait_minutes=None, apikey_id=None, **kwargs):
        """
        Prüft ob ein für den Pfad schon ein aktueller Result vorhanden ist.
        min_age kann ein Mindestalter für das result vorraussetzen
        über k(ey)w(ord)args können parameter aus dem params getestet werde (gecastet auf string)
        :type path: str
        :type apikey_id: int
        :type min_age: timedelta
        :rtype : bool
        """
        success_only = True
        if error_wait_minutes:
            success_only = False

        result = cls.get_last_call(path, apikey_id, success_only=success_only, **kwargs)

        if not result:
            return True

        if not success_only and not result.success:
            if result.created + timedelta(minutes=error_wait_minutes) < datetime.utcnow():
                return cls.check_expired(path, min_age=min_age, apikey_id=apikey_id, **kwargs)
            return False

        if min_age and result.result_timestamp + min_age < datetime.utcnow():
            return False

        return result.result_expires < datetime.utcnow() - timedelta(minutes=1)


class RedisCache(evelink.api.APICache):
    """An implementation of APICache using a redis.StrictRedis connection."""

    def __init__(self, strict_redis_connections):
        assert strict_redis_connections
        super(RedisCache, self).__init__()
        self.connection = strict_redis_connections

    def get(self, key):
        result = self.connection.get(key)
        if not result:
            rkey = "apirl_%d" % int(time.time())
            limit = self.connection.pipeline().incr(rkey).expire(rkey, 360).execute()[0]
            if limit > 28:
                time.sleep(1)  # TODO: FIXME: actually do something that makes sense here
                return self.get(key)
            return result
        return pickle.loads(result)

    def put(self, key, value, duration):
        self.connection.setex(key, duration, pickle.dumps(value))


_api = None


class EVEAPI(evelink.api.API):
    """A wrapper around the EVE API."""

    @classmethod
    def cached(cls, api_key=None):
        """
        get a (cached) api connection for this thread (celery worker)
        :rtype : EVEAPI
        """
        global _api
        if not _api:
            _api = cls()
        _api.api_key = api_key
        return _api

    def get(self, path, params=None):
        """
        :rtype : APIResultEx
        """
        data = {
            "path": path,
            "params": params,
        }

        if self.api_key:
            keyid = self.api_key[0]
            data["apikey_id"] = keyid
        else:
            keyid = None

        try:
            apiresult = super(EVEAPI, self).get(path, params)
            data["result_timestamp"] = datetime.utcfromtimestamp(apiresult.timestamp),
            data["result_expires"] = datetime.utcfromtimestamp(apiresult.expires)
            data["success"] = True
            insertid = db.engine.execute(ApiCall.__table__.insert().returning(ApiCall.__table__.c.id), data).scalar()
            return APIResultEx(result=apiresult.result, expires=apiresult.expires,
                               timestamp=apiresult.timestamp, apicallid=insertid)
        except evelink.api.APIError as apierror:
            data["api_error_code"] = apierror.code
            data["api_error_message"] = apierror.message
            # TODO: save api key error count
            # with db.engine.begin() as conn:
            #    keytable = ApiKey.__table__
            #    update = keytable.update().where(keytable.c.keyid == keyid)
            #    if keyid and int(apierror.code) in [222, 203]:
            #        update = update.values(error_count=99)
            #    else:
            #        update = update.values(error_count=keytable.c.error_count + 1)
            #    conn.execute(update)
            #    conn.execute(ApiCall.__table__.insert(), data)
            raise apierror
        except ConnectionError as e:
            data["http_error_code"] = e.errno
            if hasattr(e, "message"):
                data["http_error_message"] = str(e.message)
            else:
                data["http_error_message"] = str(e)
            with db.engine.begin() as conn:
                conn.execute(ApiCall.__table__.insert(), data)
            raise e
        except requests.HTTPError as e:
            data["http_error_code"] = e.response.status_code
            if hasattr(e, "message"):
                data["http_error_message"] = str(e.message)
            else:
                data["http_error_message"] = str(e)
            with db.engine.begin() as conn:
                conn.execute(ApiCall.__table__.insert(), data)
            raise e

import inject
import applauncher.kernel
from applauncher.kernel import InjectorReadyEvent
from mongoengine import connect
import logging


class MongoEngineBundle(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config_mapping = {
            "mongoengine": {
                "db": "default",
                "host": "localhost",
                "port": 27017,
                "username": "",
                "password": "",
                "ssl": False,
                "replica_set": "",
                "authentication_source": "",
                "retry_writes": False,
                "connect": True
            }
        }
        
        self.event_listeners = [
            (InjectorReadyEvent, self.event_listener)
        ]

    @staticmethod
    def _value_or_none(value):
        return None if value == "" or value == "None" else value

    def event_listener(self, event):
        config = inject.instance(applauncher.kernel.Configuration)
        mongo = config.mongoengine
        if mongo.connect:
            host = self._value_or_none(mongo.host)
            if host and host.startswith("mongodb://"):
                kwargs = {
                    "host": host
                }
            else:
                kwargs = {
                    "db": self._value_or_none(mongo.db),
                    "host": host,
                    "port": self._value_or_none(mongo.port),
                    "username": self._value_or_none(mongo.username),
                    "password": self._value_or_none(mongo.password),
                    "ssl": bool(mongo.ssl) if self._value_or_none(mongo.ssl) is not None else None,
                    "replicaSet": self._value_or_none(mongo.replica_set),
                    "authentication_source": self._value_or_none(mongo.authentication_source),
                    "retryWrites": self._value_or_none(mongo.retry_writes)
                }
            connect(
                connect=False,
                **{k: v for k, v in kwargs.items() if v is not None}
            )
            self.logger.info("Connected to mongo")
        else:
            self.logger.info("Not connected to mongo because connect is false")


 

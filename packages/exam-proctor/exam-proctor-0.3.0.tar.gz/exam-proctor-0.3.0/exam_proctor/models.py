from playhouse import sqliteq
from datetime import datetime, timedelta
import peewee
from . import glb


db = sqliteq.SqliteQueueDatabase(glb.get_path('default.db'))


class Session(peewee.Model):
    ts_create = peewee.DateTimeField(default=datetime.now)
    ts_expire = peewee.DateTimeField(null=True, default=None)
    session_id = peewee.CharField(max_length=128)
    service_url = peewee.CharField(max_length=1023)
    redirect_url = peewee.CharField(max_length=1023)

    class Meta:
        database = db


class Video(peewee.Model):
    session = peewee.ForeignKeyField(Session, index=True)
    ts_create = peewee.DateTimeField()
    ts_end = peewee.DateTimeField(default=None, null=True)
    position = peewee.IntegerField()
    type = peewee.CharField(max_length=20)
    name = peewee.CharField(max_length=64)
    size = peewee.IntegerField(null=True, default=None)
    hash = peewee.CharField(max_length=41, default=None, null=True)
    ts_update = peewee.DateTimeField(default=None, null=True)
    upload_url = peewee.CharField(max_length=511, null=True, default=None)
    ts_update_upload = peewee.DateTimeField(default=None, null=True)

    class Meta:
        database = db


class Process(peewee.Model):
    session = peewee.ForeignKeyField(Session, index=True)
    ts_create = peewee.DateTimeField(default=datetime.now)
    ts_start = peewee.DateTimeField(null=True)
    ts_end = peewee.DateTimeField(default=None, null=True)
    pid = peewee.IntegerField()
    name = peewee.CharField()
    connections = peewee.IntegerField()
    command = peewee.CharField(max_length=2000)
    ts_update_create = peewee.DateTimeField(default=None, null=True)
    ts_update_end = peewee.DateTimeField(default=None, null=True)

    class Meta:
        database = db


db.create_tables([Session, Video, Process])

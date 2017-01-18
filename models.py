import peewee
from playhouse.migrate import *

database_sqlite = peewee.SqliteDatabase("temporary.db")

class City(peewee.Model):
    rank = peewee.IntegerField(null=False)
    city = peewee.TextField(null=False)
    country = peewee.TextField(null=False)
    tourists_millions = peewee.FloatField(default=0,null=False)
    ig_link = peewee.TextField(null=False)
    photos_path = peewee.TextField(null=True)

    class Meta:
        database = database_sqlite

database_sqlite.create_tables([City], safe=True)

from peewee import (
    Model,
    SqliteDatabase,
    AutoField,
    TextField,
    DateTimeField,
)


# from pathlib import Path
# home_dir =

# Create a database instance

from pathlib import Path
import os

basedir = Path(os.path.dirname(__file__))
db_path = basedir / "carpetdb.sqlite3"

conn = SqliteDatabase(str(db_path))


class BaseModel(Model):
    class Meta:
        database = conn


# TODO: add support for multiple monitors
# class Screenshot(BaseModel):
#     sid = AutoField()
#     filepath = TextField()
#     text = TextField()  # ocr text


class Capture(BaseModel):
    cid = AutoField()
    timestamp = DateTimeField()
    filepath = TextField()  # screenshot filepath


def init_db():
    conn.connect()
    conn.create_tables(
        [
            Capture,
        ]
    )

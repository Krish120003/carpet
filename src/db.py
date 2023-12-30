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
conn = SqliteDatabase("carpetdb.sqlite3")


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


conn.connect()
conn.create_tables(
    [
        Capture,
    ]
)


if __name__ == "__main__":
    Capture.create(timestamp="2020-01-01 00:00:00", filepath="tes2t.png").save()
    conn.close()

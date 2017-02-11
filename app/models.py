from .db import db
import datetime
from peewee import *

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True, null=False)
    email = CharField(unique=True)

class DataType(BaseModel):
    name = CharField(unique=True)

class TagSet(BaseModel):
    name = CharField(null=False)
    display_name = CharField(null=False)
    data_type = ForeignKeyField(DataType, null=False)
    data_info = CharField(null=False)
    version = IntegerField(null=False, default=1)

    class Meta:
        indexes = (
            # create a unique on name/version
            (('name', 'version'), True),
        )

class Tag(BaseModel):
    name = CharField(unique=True, null=False)
    tagset = ForeignKeyField(TagSet, null=False)

class TagRun(BaseModel):
    user = ForeignKeyField(User, related_name='tagrun')
    tagset = CharField(null=False)
    data_item = IntegerField(null=False)
    response = IntegerField(null=False)
    created_date = DateTimeField(default=datetime.datetime.now)

# TODO: This should live in a setup script or we should use Peewee's migration
# code.
def create_tables():
    db.connect()
    db.create_tables([User, TagRun, DataType, TagSet, Tag])

def add_dummy_values():
    from_local_dir = DataType(
        name="ImagesFromLocalDirectory"
    )
    from_local_dir.save()
    ts = TagSet(
        name="kittendemo",
        display_name="Is it a kitten?",
        data_type=from_local_dir,
        data_info="kitten",
    )
    ts.save()
    tags = ["Kitten", "Not Kitten", "I can't tell", "Broken image"]
    for t in tags:
        tag = Tag(name=t, tagset=ts)
        tag.save()

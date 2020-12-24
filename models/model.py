from peewee import *

db = SqliteDatabase('ancient.db')


class Author(Model):
    id = CharField(primary_key=True)
    name = CharField()
    description = CharField(null=True, default='')
    short_description = CharField(null=True, default='')
    desc = CharField(null=True, default='')
    dynasty = CharField()

    class Meta:
        database = db


class Word(Model):
    id = AutoField(primary_key=True)
    ci = CharField(null=True, default='')
    explanation = CharField(null=True, default='')
    example = CharField(null=True, default='')
    pinyin = CharField(null=True, default='')
    word = CharField(null=True, default='')
    abbreviation = CharField(null=True, default='')
    riddle = CharField(null=True, default='')
    answer = CharField(null=True, default='')
    derivation = CharField(null=True, default='')
    word_type = CharField()

    class Meta:
        database = db

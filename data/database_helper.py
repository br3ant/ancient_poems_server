import json
import os
import uuid
from models.model import *

word_data = {
    'word_ci': 'ci.json',
    'word_idiom': 'idiom.json'
}

author_data = {
    'song_poem': 'authors.song.json',
    'song_ci': 'author.song.json',
    'tang_poem': 'authors.tang.json',
}

poem_data = {
    'song_ci': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/ci',
    'tang_poem': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/json',
    'song_poem': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/json'
}


def init_database():
    db.connect()

    db.create_tables([Author, Word, Poem])

    for author_type, json_name in author_data.items():
        init_author(author_type, json_name)

    for word_type, json_name in word_data.items():
        init_word(word_type, json_name)

    for poem_type, json_name in poem_data.items():
        init_poem(poem_type, json_name)


def init_author(author_type, json_name):
    print(f'开始初始化 author_type = {author_type}')
    with open(os.path.join('data', json_name), 'r') as f:
        authors = json.load(f)
        with db.atomic():
            for author in authors:
                try:
                    Author().create(**author, dynasty=author_type)
                except IntegrityError:
                    Author().replace(**author, dynasty=author_type)


def init_word(word_type, json_name):
    print(f'开始初始化 word_type = {word_type}')
    with open(os.path.join('data', json_name), 'r') as f:
        words = json.load(f)
        with db.atomic():
            for word in words:
                try:
                    Word().create(**word, word_type=word_type)
                except IntegrityError:
                    Word().replace(**word, word_type=word_type)


def init_poem(poem_type, path):
    print(f'开始初始化 poem_type = {poem_type}')
    if poem_type == 'song_ci':
        for json_file in os.listdir(path):
            if 'ci.song' in json_file:
                add_poems(poem_type, os.path.join(path, json_file))
    elif poem_type == 'tang_poem':
        for json_file in os.listdir(path):
            if 'poet.tang' in json_file:
                add_poems(poem_type, os.path.join(path, json_file))
    elif poem_type == 'song_poem':
        for json_file in os.listdir(path):
            if 'poet.song' in json_file:
                add_poems(poem_type, os.path.join(path, json_file))


def add_poems(poem_type, json_file):
    with open(json_file, 'r') as f:
        poems = json.load(f)
        with db.atomic():
            for poem in poems:
                try:
                    if 'song_ci' == poem_type:
                        Poem().create(**poem, dynasty=poem_type, id=uuid.uuid1())
                    else:
                        Poem().create(**poem, dynasty=poem_type)
                except IntegrityError:
                    Poem().replace(**poem, dynasty=poem_type)


def trans_db_model(value):
    return value.__data__


def query_words(word_type, page, limit):
    try:
        return Word.select(Word.ci, Word.explanation).where(Word.word_type == word_type).paginate(page, limit).dicts()
    except Exception as e:
        print(f"query ERROR e = {e}")
        return None


def query_author(name):
    try:
        return Author.get_or_none(Author.name == f'{name}').__data__
    except Exception as e:
        print(f"query ERROR e = {e}")
        return None


def query_poems(dynasty, page, limit):
    try:
        return Poem.select().where(Poem.dynasty == dynasty).paginate(page, limit).dicts()
    except Exception as e:
        print(f"query ERROR e = {e}")
        return None

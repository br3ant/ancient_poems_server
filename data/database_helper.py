import json
import os
from models.model import *

word_data = {
    'word_ci': 'ci.json',
    'word_idiom': 'idiom.json'
}

author_data = {
    'song_poem': 'authors.song.json'
}


def init_database():
    db.connect()

    db.create_tables([Author, Word])

    for author_type, json_name in author_data.items():
        init_author(author_type, json_name)

    for word_type, json_name in word_data.items():
        init_word(word_type, json_name)


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


def trans_db_model(value):
    return value.__data__


def query_poems(dynasty, page, limit):
    # try:
    #     return Author.get(Author.name == f'{name}')
    # except Exception as e:
    #     print(f"query ERROR e = {e}")
    #     return None
    pass


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


if __name__ == '__main__':
    init_database()

    values = query_author('朱存')
    print(values)

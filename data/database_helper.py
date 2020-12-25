import json
import os
from models.model import *

word_data = {
    'word_ci': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-xinhua-master/data/ci.json',
    'word_idiom': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-xinhua-master/data/idiom.json',
    'word_xiehouyu': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-xinhua-master/data/xiehouyu.json',
    'word_word': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-xinhua-master/data/word.json',
}

author_data = {
    'song_poem': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/json/authors.song.json',
    'song_ci': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/ci/author.song.json',
    'tang_poem': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/json/authors.tang.json',
}

poem_data = {
    'song_ci': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/ci',
    'tang_poem': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/json',
    'song_poem': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/json',
    'yuan_qu': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/yuanqu/yuanqu.json',
    'shi_jing': '/Users/houqiqi/Documents/WorkSpace/Python/chinese-poetry-master/shijing/shijing.json',
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
    with open(json_name, 'r') as f:
        authors = json.load(f)
        with db.atomic():
            for author in authors:
                try:
                    Author().create(dynasty=author_type, name=author.get('name'), desc=author.get('desc'),
                                    description=author.get('description'),
                                    short_description=author.get('short_description'))
                except IntegrityError:
                    pass


def init_word(word_type, json_name):
    print(f'开始初始化 word_type = {word_type}')
    with open(json_name, 'r') as f:
        words = json.load(f)
        with db.atomic():
            for word in words:
                try:
                    Word().create(word_type=word_type, ci=word.get('ci'), explanation=word.get('explanation'),
                                  example=word.get('example'), pinyin=word.get('pinyin'), word=word.get('word'),
                                  abbreviation=word.get('abbreviation'), riddle=word.get('riddle'),
                                  answer=word.get('answer'),
                                  derivation=word.get('derivation'), )
                except IntegrityError:
                    pass


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
    elif poem_type == 'yuan_qu' or poem_type == 'shi_jing':
        add_poems(poem_type, path)


def add_poems(poem_type, json_file):
    with open(json_file, 'r') as f:
        poems = json.load(f)
        with db.atomic():
            for poem in poems:
                try:
                    Poem().create(dynasty=poem_type, author=poem.get('author'), paragraphs=poem.get('paragraphs'),
                                  rhythmic=poem.get('rhythmic'),
                                  title=poem.get('title'), chapter=poem.get('chapter'), tags=poem.get('tags'),
                                  prologue=poem.get('prologue'),
                                  content=poem.get('content'), section=poem.get('section'))
                except IntegrityError:
                    pass


def trans_db_model(value):
    return value.__data__


def query_words(word_type, page, limit):
    try:
        return Word.select().where(Word.word_type == word_type).paginate(page, limit).dicts()
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


def query_authors(dynasty, page, limit):
    try:
        return Author.select().where(Author.dynasty == dynasty).paginate(page, limit).dicts()
    except Exception as e:
        print(f"query ERROR e = {e}")
        return None


def query_poems_count():
    return Poem.select().limit(10).dicts()

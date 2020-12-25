from data import database_helper

if __name__ == '__main__':
    # values = database_helper.query_words('word_ci', 1, 10)
    # print(list(values))
    # for v in values:
    #     print(v)
    # var = database_helper.query_author('苏轼')
    # print(var)

    for word in database_helper.word_data.keys():
        print(list(database_helper.query_words(word, 1, 10)))

    for author in database_helper.author_data.keys():
        print(list(database_helper.query_authors(author, 1, 10)))

    for poem in database_helper.poem_data.keys():
        print(list(database_helper.query_poems(poem, 1, 10)))



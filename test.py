from data import database_helper

if __name__ == '__main__':
    # values = database_helper.query_words('word_ci', 1, 10)
    # print(list(values))
    # for v in values:
    #     print(v)
    var = database_helper.query_author('朱存')
    print(var)

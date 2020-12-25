from fastapi import FastAPI
from response import response
from data import database_helper

app = FastAPI()


@app.get("/")
def read_root():
    return response.SuccessResponse('Hello Word!!')


@app.get("/getPoems")
def get_poems(dynasty: str = None, page: int = 1, limit: int = 10):
    if dynasty:
        values = database_helper.query_poems(dynasty, page, limit)
        return response.SuccessResponse(list(values))
    else:
        return response.ErrorResponse(0, 'dynasty 不能为空')


@app.get("/getPoemAuthor")
def get_poem_author(name: str = None):
    if name:
        value = database_helper.query_author(name)
        if value:
            return response.SuccessResponse(value)
        else:
            return response.ErrorResponse(0, f'没有找到{name}')
    else:
        return response.ErrorResponse(0, 'name 不能为空')


@app.get("/getWords")
def get_words(word_type: str = None, page: int = 1, limit: int = 10):
    if word_type:
        values = database_helper.query_words(word_type, page, limit)
        return response.SuccessResponse(list(values))
    else:
        return response.ErrorResponse(0, 'word_type 不能为空')

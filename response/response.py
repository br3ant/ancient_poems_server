import json


class BaseResponse:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def to_string(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class SuccessResponse(BaseResponse):

    def __init__(self, data):
        super().__init__(1, '请求成功')
        self.data = data


class ErrorResponse(BaseResponse):
    def __init__(self, code, message):
        super().__init__(code, message)

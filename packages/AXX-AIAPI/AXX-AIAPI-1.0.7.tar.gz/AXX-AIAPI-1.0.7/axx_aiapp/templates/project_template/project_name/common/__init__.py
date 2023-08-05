from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

geh = Blueprint('common', __name__)


class APIResponse:
    __default_succeed = {
        'code': 200,
        'msg': 'Success',
        'data': None
    }
    __default_failed = {
        'code': 500,
        'msg': 'Server Failed',
        'data': None
    }

    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def success(cls, data=None):
        rsp = dict(cls.__default_succeed)
        if data is not None:
            rsp['data'] = data
        return rsp

    @classmethod
    def failed(cls, msg=None, code=None):
        rsp = dict(cls.__default_failed)
        if code is not None:
            rsp['code'] = code
        if msg is not None:
            rsp['msg'] = msg
        return rsp


class AIException(Exception):

    def __init__(self, message, code=None):
        Exception.__init__(self)
        self.message = message
        self.code = code

    def get_response(self):
        return APIResponse.failed(self.message, self.code)


@geh.app_errorhandler(Exception)
def handle_invalid_usage(error):
    print(type(error))
    print(error)
    response = None
    if isinstance(error, AIException):
        response = jsonify(error.get_response())
    elif issubclass(type(error), HTTPException):
        response = jsonify(APIResponse.failed(error.name, error.code))
    else:
        response = jsonify(APIResponse.failed())
    return response

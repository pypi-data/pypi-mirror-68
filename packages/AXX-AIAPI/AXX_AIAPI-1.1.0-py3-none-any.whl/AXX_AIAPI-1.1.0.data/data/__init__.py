import json

from flask import Blueprint, jsonify, current_app
from werkzeug.exceptions import HTTPException

geh = Blueprint('common', __name__)


class APIResponse:
    """
    接口响应通用格式
    含 code（响应状态码）msg（响应消息）data（响应数据三部分）
    """
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

    @classmethod
    def success(cls, data=None):
        """
        返回成功响应
        :param data:
        :return:
        """
        rsp = dict(cls.__default_succeed)
        if data is not None:
            rsp['data'] = data
        return rsp

    @classmethod
    def failed(cls, msg=None, code=None):
        """
        返回失败响应
        :param msg:
        :param code:
        :return:
        """
        rsp = dict(cls.__default_failed)
        if code is not None:
            rsp['code'] = code
        if msg is not None:
            rsp['msg'] = msg
        return rsp


class AIException(Exception):
    """
    自定义异常类，抛出此异常可被全局异常处理器捕捉并包装成通用响应体返回
    """

    def __init__(self, message, code=None):
        Exception.__init__(self)
        self.message = message
        self.code = code

    def get_response(self):
        return APIResponse.failed(self.message, self.code)


@geh.app_errorhandler(AIException)
def handle_invalid_usage(error):
    """
    拦截所有AIException类型异常并进行包装返回
    :param error: AIException类型异常
    :return:
    """
    response = None
    if isinstance(error, AIException):
        response = jsonify(error.get_response())
    current_app.logger.error(str(response.data, encoding="utf-8"))
    return response


@geh.app_errorhandler(HTTPException)
def handle_invalid_usage(error):
    """
    拦截所有HTTPException异常并进行包装返回，包含框架HTTP协议自身产生的，以及代码中通过abort抛出的
    :param error:
    :return:
    """
    response = None
    if issubclass(type(error), HTTPException):
        response = jsonify(APIResponse.failed(error.name, error.code))
    current_app.logger.error(str(response.data, encoding="utf-8"))
    return response

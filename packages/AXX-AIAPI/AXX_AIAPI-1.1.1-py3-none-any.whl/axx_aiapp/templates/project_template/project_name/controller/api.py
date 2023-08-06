from flask import Blueprint, jsonify, current_app, request, abort
from utils.constants import METHODTYPE
from common import APIResponse, AIException

api = Blueprint('api', __name__, url_prefix='/api')


# 正常调用演示 POST方法
@api.route('/', methods=[METHODTYPE.POST, METHODTYPE.GET])
def api_index():
    current_app.logger.info(f'{request.method} api.index')
    data = request.json
    return APIResponse.success(data)


# 返回自定义错误演示1
@api.route('/err', methods=[METHODTYPE.GET])
def api_failed():
    current_app.logger.info(f'{request.method} api.failed')
    data = request.args
    return APIResponse.failed('错误信息', 1001)


# 返回自定义异常
@api.route('/exc', methods=[METHODTYPE.GET])
def api_exception():
    current_app.logger.error(f'{request.method} api.exc')
    data = request.args
    if data.get('exc_flag'):
        raise AIException('内部异常', 1005)
    return APIResponse.success(data)


# 使用abort抛出http异常
@api.route('/exc2', methods=[METHODTYPE.GET])
def api_exception2():
    current_app.logger.error(f'{request.method} api.exc2')
    print('after')
    data = request.args
    if data.get('exc_flag'):
        abort(400)
    return APIResponse.success(data)

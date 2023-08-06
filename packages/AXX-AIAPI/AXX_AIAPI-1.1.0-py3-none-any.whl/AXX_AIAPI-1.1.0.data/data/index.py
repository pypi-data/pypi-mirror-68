from flask import Blueprint, current_app, request

from common import APIResponse
from utils.constants import METHODTYPE

index = Blueprint('index', __name__, '/index')


@index.route('/', methods=[METHODTYPE.POST])
def index_home():
    current_app.logger.info(f'{request.method} index.index')
    data = request.json
    return APIResponse.success(data)

import os
from flask import Blueprint, current_app, render_template, request
from utils.constants import METHODTYPE

index = Blueprint('index', __name__, '/index')


@index.route('/', methods=[METHODTYPE.GET, METHODTYPE.POST])
def index_home():
    current_app.logger.info(f'{request.method} controller.index')
    if request.method == METHODTYPE.GET:
        data = request.args
        return jsonify({"success": True, "name": 'controller.index', 'data': data})
    else:
        data = request.json  # for request that POST with application/json
        return jsonify({"success": True, "name": 'controller.index', 'data': data})

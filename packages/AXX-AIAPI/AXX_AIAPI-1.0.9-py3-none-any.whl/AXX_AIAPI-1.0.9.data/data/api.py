from flask import Blueprint, jsonify, current_app, request, abort
from utils.constants import METHODTYPE


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=[METHODTYPE.GET, METHODTYPE.POST])
def api_index():
    current_app.logger.info(f'{request.method} api.index')

    if request.method == METHODTYPE.GET:
        data = request.args
        return jsonify({"success": True, "name": 'controller.index', 'data': data})
    else:
        data = request.json     # for request that POST with application/json
        return jsonify({"success": True, "name": 'controller.index', 'data': data})
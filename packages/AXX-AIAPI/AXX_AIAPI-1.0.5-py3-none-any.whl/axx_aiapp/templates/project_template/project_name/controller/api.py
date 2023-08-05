from flask import Blueprint, jsonify, current_app, request, abort
from utils.constants import METHODTYPE


api = Blueprint('controller', __name__, url_prefix='/controller')


@api.route('/', methods=[METHODTYPE.GET, METHODTYPE.POST])
def api_index():
    current_app.logger.info(f'{request.method} controller.index')

    if request.method == METHODTYPE.GET:
        data = request.args
        return jsonify({"success": True, "name": 'controller.index', 'data': data})
    else:
        data = request.json     # for request that POST with application/json
        return jsonify({"success": True, "name": 'controller.index', 'data': data})


@api.route('/upload', methods=[METHODTYPE.POST])
def api_upload():
    current_app.logger.info(f'{request.method} controller.upload')
    if request.method == METHODTYPE.GET:
        abort(405)

    files = request.files       # for request that POST with multipart/form-data's files
    for file in files:
        print(file.readline())
    data = request.form         # for request that POST with multipart/form-data's data
    return jsonify({"success": True, "name": 'controller.upload', 'data': data, 'files': files})


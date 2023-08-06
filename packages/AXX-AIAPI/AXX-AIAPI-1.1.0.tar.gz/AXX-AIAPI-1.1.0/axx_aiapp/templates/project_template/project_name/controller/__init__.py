from .index import index
from .api import api
from common import geh

bps = [index, api, geh]


def init_blue_print(app):
    for bp in bps:
        app.register_blueprint(bp)

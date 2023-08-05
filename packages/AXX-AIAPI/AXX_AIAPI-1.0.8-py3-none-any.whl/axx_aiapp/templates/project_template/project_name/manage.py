import os
import logging
import sys
from flask import Flask
from controller import init_blue_print
from config import config, G, config_log
from utils import parse_args


def create_app():
    logger = None
    app = Flask(__name__)
    env = os.environ.get('AI_ENV', 'default')
    app.config.from_object(config.get(env))
    init_blue_print(app)
    config_log()
    # if config.get(env) == 'prd':
    logger = logging.getLogger('gunicorn.error')
    # else:
    #     logger = logging.getLogger('flask.app.module')
    G.logger = logger
    return app


def init_python_path(_file_):
    package_dir = os.path.join(os.path.dirname(_file_), '../')
    abs_path = os.path.abspath(package_dir)
    if abs_path not in sys.path:
        sys.path.insert(0, abs_path)


init_python_path(__file__)

__all__ = ['main']


def main():
    app = create_app()
    args = parse_args()

    if args.cmd.isdigit():
        cmd = 'runserver'
        port = int(args.cmd)
    else:
        cmd = args.cmd
        port = args.port if args.port else 8080

    if cmd == 'runserver':
        app.run('0.0.0.0', port)
        app.logger.info(f'run server at port {port}')
    else:
        print('run command error')


if __name__ == '__main__':
    main()

import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="run app command!")
    parser.add_argument("-p", "--port", help="bind port!", type=int)
    return parser.parse_args()


def get_abs_dir(_file_):
    return os.path.abspath(os.path.dirname(_file_))

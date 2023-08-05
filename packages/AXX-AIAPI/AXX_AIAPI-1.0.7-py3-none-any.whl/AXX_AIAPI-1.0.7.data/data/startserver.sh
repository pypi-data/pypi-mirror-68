#!/usr/bin/env bash
gunicorn server:app -c ./config/gunicorn.config.py
#!/bin/bash

gunicorn --log-level debug --chdir app --preload -b 0.0.0.0:8000 wsgi:app

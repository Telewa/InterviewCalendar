#!/usr/bin/env bash

coverage erase
coverage run --parallel-mode --concurrency=multiprocessing --rcfile=./backend/.coveragerc ./backend/manage.py test backend -v 3 --parallel=3
coverage combine
coverage report -m
codecov

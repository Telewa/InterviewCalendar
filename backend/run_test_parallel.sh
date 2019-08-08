#!/usr/bin/env bash

coverage erase
coverage run --parallel-mode --concurrency=multiprocessing --rcfile=./.coveragerc manage.py test --settings=configuration.settings -v 3 --parallel=3
coverage combine
coverage report -m
coveralls
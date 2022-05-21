#!/bin/bash

poetry run pytest --cov-branch --cov-report term-missing --cov=pinferencia tests/unittest

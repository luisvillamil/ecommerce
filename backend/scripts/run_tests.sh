#!/bin/bash
poetry run python -m pytest --cov-report html --cov=ecommerce "$@"
#!/bin/bash
pip install poetry pre-commit && \
    pre-commit install && \
    poetry install && \
    poetry run pip install streamlit playwright && \
    poetry run playwright install && \
    poetry run playwright install-deps

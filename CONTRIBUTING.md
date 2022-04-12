# Contributing to Pinference

## Issues Types

There are mainly three types of issues:

- Bugfix
- Feature
- Documentation

For simple bugs, an issue with a pull request is welcomed.

For complex bugs and new features, first create an issue and start a discussion. Once all the details resolved, we can start developing.

For documentation, any improvement and translations are welcome. Please create an issue and let's make it happen.

## Setup the Environment

### Python

**Pinferencia** uses [poetry](https://github.com/python-poetry/poetry) to manage dependencies, build and publish.

Install dependencies:

```bash
poetry install --dev
```

### Documentation

Start the documentation server:

```bash
mkdocs serve
```

## Test

Please run the following command to test your codes. Before merging the pull request, make sure you have a 100% code coverage.

```bash
pytest --cov-branch --cov-report term-missing --cov=pinferencia
```
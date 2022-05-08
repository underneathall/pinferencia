# Contributing to Pinferencia

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
poetry install
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

## Coding Requirements

The most important rule is:

> Keep your codes pythonic, keep your tests simple stupid.

1. When writing codes to implement a feature or an improvements, or fix a bug, write the codes in a pythonic way. Format with black, lint with flake8. Use the pre-commit hook.

2. When writing testing codes, keep them simple, and stupid. Redundancy is totally okay if it helps keep the tests simple and easier to understand. Don't write tests with a deep chain of dependent codes. It will keep you jumping from one file to another, and end up a big mess.

### Why?

When you write functioning codes (the codes implement the logics), you will organize some codes into a module/function for others to call. This creates dependencies. When the dependencies get complicated, which it almost always does, it becomes harder to make modifications to these codes without breaking other codes.

To avoid this potential risk, we write tests to make sure everything is still working after the change of the codes.

Ok, if you do the same thing with your test codes, like using a lot of dependencies. Oh boy, it will drive you crazy in the end. Once you need to modify a test, another two failed. And you will make mistakes modifying the tests sooner or later.

For example, if you make changes to a lot of tests at one time, some tests may not be as sensitive (perhaps it is even wrong, because you're so busy fixing the tests without knowing if you're doing it correctly) as before, because no codes is monitoring the test codes.

Should you write codes to test your testing codes? Ironic, right?

So, make the tests simple. Even you need to do some `copy & paste` to update the tests, at least you're doing it step by step without introducing more unexpected failures.

It may sound strange.

However the two most important things of a test is: clear and easy to maintain.

Keeping it simple stupid will help you achieve these two goals. Sometimes, stupid is clever.

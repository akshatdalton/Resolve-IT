# Resolve-IT

Resolve-IT is a command line tool that fetches Stack Overflow results when an exception is thrown or when a query is made. Run your python file with `resolveit` and see the results.

<!-- [![coverage status](https://img.shields.io/codecov/c/github/zulip/zulip/master.svg)](https://codecov.io/gh/zulip/zulip/branch/master) -->
[![GitHub Actions build status](https://github.com/akshatdalton/Resolve-IT/actions/workflows/resolveit-ci.yml/badge.svg?branch=main)](https://github.com/akshatdalton/Resolve-IT/actions/workflows/resolveit-ci.yml?query=branch%3main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/akshatdalton/Resolve-IT/)

![resolveit](docs/resolveit.gif)

---

## How to use it?

That's pretty easy. Follow the following setup steps:

```
git clone https://github.com/akshatdalton/Resolve-IT.git
virtualenv venv
source venv/bin/activate
python3 setup.py install
```

Once you have run all the commands and results are fine, we are all set to run the tool:

```
(venv) $ resolveit -f <your_file_name>
```

## Other usage

1. You can use this tool to search results for query from Stack Overflow:

    ```
    (venv) $ resolveit -q "difference between json.dump and json.dumps"
    ```

2. Want to debug specific functions or part of the code? Run this package as context manager:

    - As function decorator:
      ```python3
      from resolveit import debug

      @debug
      def foo():
        # Here goes the code ...
      ```

    - As `with` statement:
      ```python3
        from resolveit import ResolveIT

        with ResolveIT():
            # Here goes the code ...
      ```

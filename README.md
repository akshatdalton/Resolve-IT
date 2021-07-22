# Resolve-IT

Resolve-IT is a command line tool that fetches Stack Overflow results when an exception is thrown or when a query is made. Run your python file with `resolveit` and see the results.

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


import os
import sys
import traceback
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from typing import Type
from unittest import TestCase, main, mock

RESOLVEIT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
sys.path.append(RESOLVEIT_PATH)

from resolveit import app


class TestApp(TestCase):
    EXCEPTIONS = [
        ArithmeticError,
        AssertionError,
        AttributeError,
        ImportError,
        MemoryError,
        NameError,
        ReferenceError,
        RuntimeError,
        SyntaxError,
        TypeError,
        ValueError,
    ]

    def test_get_actual_error(self) -> None:
        EXCEPTION_MESSAGE = "This is a regular exception message"

        def get_expected_error(exception: Type[Exception]) -> str:
            exception_name = exception.__name__
            return f"{exception_name}: {EXCEPTION_MESSAGE}"

        for exception in self.EXCEPTIONS:
            try:
                raise exception(EXCEPTION_MESSAGE)
            except Exception:
                stack_trace = traceback.format_exc()

            actual_error = app.get_actual_error(stack_trace)
            expected_error = get_expected_error(exception)
            self.assertEqual(actual_error, expected_error)

    def test_app_main(self) -> None:
        app.launch_interface = mock.MagicMock()
        query = "This is a normal query"
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(file=None, query=query),
        ):
            app.main()
            app.launch_interface.assert_called_once_with(query)

        app.launch_interface.reset_mock()
        file_path = "tests/fixtures/fixture1.py"
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(file=file_path, query=None),
        ):
            app.main()
            app.launch_interface.assert_called_once_with(
                "TypeError: must be str, not list"
            )

        file_path = "tests/fixtures/fixture2.py"
        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(file=file_path, query=None),
        ), redirect_stdout(StringIO()) as stdout, self.assertRaises(SystemExit) as e:
            app.main()
            self.assertEqual(e.exception.code, 1)
            self.assertEqual(
                stdout.getvalue(),
                f"Congratulations! Your file: {file_path} ran successfully. ✨ 🍰 ✨",
            )

        with mock.patch(
            "argparse.ArgumentParser.parse_args",
            return_value=Namespace(file=None, query=None),
        ), mock.patch("argparse.ArgumentParser.print_help") as m:
            app.main()
            m.assert_called_once()


if __name__ == "__main__":
    main()

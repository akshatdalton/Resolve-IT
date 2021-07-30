import os
import sys
from unittest import TestCase, main, mock

RESOLVEIT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
sys.path.append(RESOLVEIT_PATH)

from fixtures.fixture3 import execute_resolveit_as_context_manager

from resolveit import ResolveIT, app, debug
from resolveit.settings import do_suppress_animation


class TestResolveIT(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        do_suppress_animation()

    def test_resolveit_as_class_context_manager(self) -> None:
        app.launch_interface = mock.MagicMock()

        with ResolveIT():
            execute_resolveit_as_context_manager()

        app.launch_interface.assert_called_once_with("TypeError: must be str, not list")
        app.launch_interface.reset_mock()

        # Here we ensure that ResolveIT captures only the know errors.
        with self.assertRaises(ValueError):
            with ResolveIT():
                a = "foo"
                b = "bar"
                a += b
            raise ValueError("foo bar baz")

        app.launch_interface.assert_not_called()

    def test_resolveit_as_decorator_context_manager(self) -> None:
        app.launch_interface = mock.MagicMock()

        @debug
        def resolveit_as_decorator_context_manager() -> None:
            execute_resolveit_as_context_manager()

        resolveit_as_decorator_context_manager()
        app.launch_interface.assert_called_once_with("TypeError: must be str, not list")
        app.launch_interface.reset_mock()

        # Here we ensure that debug captures only the know errors.
        with self.assertRaises(ValueError):

            @debug
            def simple_function() -> None:
                a = "foo"
                b = "bar"
                a += b

            simple_function()
            raise ValueError("foo bar baz")

        app.launch_interface.assert_not_called()


if __name__ == "__main__":
    main()

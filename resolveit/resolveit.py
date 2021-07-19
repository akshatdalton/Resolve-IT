import subprocess
import sys
from argparse import ArgumentParser
from subprocess import PIPE
from types import TracebackType
from typing import Any, Callable, Optional, Type

from resolveit.cli_output import Interface
from resolveit.fetch_results import parse_and_get_results


def display_success_message(file: str) -> None:
    print(f"Congratulations! Your file: {file} ran successfully. ✨ 🍰 ✨")


def get_actual_error(stderr: str) -> str:
    # Most part of the errors are just stack traceback calls.
    # We just need the actual error message.
    return stderr.split("\n")[-2].strip()


def launch_interface(error_msg: str) -> None:
    result_links = parse_and_get_results(error_msg)
    Interface(result_links)


class ResolveIT(object):
    def __init__(self, func: Optional[Callable[..., Any]] = None) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Optional[Callable[..., Any]]:
        if self.func is not None:
            try:
                return self.func(*args, **kwargs)
            except Exception as e:
                error_type = type(e).__name__
                error_msg = f"{error_type}: {str(e)}"
                launch_interface(error_msg)
        return None

    def __enter__(self) -> None:
        pass

    def __exit__(
        self, exc_type: Type[Any], exc_value: str, exc_traceback: TracebackType
    ) -> bool:
        if exc_traceback is not None:
            error_msg = f"{exc_type.__name__}: {exc_value}"
            launch_interface(error_msg)
            return True
        return False


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="A CLI tool that fetches Stack Overflow results when an exception is thrown."
    )
    parser.add_argument(
        "-f", "--file", type=str, required=False, help="File name to debug."
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        required=False,
        help="A query to search on Stack Overflow.",
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if args.file is not None:
        language = "python3"
        terminal_command = [language, args.file]
        # We keep `check=False` so that  we do not show the traceback
        # calls to this process when the execution of file fails.
        process = subprocess.run(
            terminal_command, stdout=PIPE, stderr=PIPE, encoding="UTF-8"
        )

        if process.returncode == 0:
            display_success_message(args.file)
            sys.exit()

        actual_error = get_actual_error(process.stderr)
        launch_interface(actual_error)
    elif args.query is not None:
        launch_interface(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

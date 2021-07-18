import subprocess
import sys
from argparse import ArgumentParser
from subprocess import PIPE
from typing import Dict, List

from cli_output import Interface
from fetch_results import parse_and_get_results


def display_success_message(file: str) -> None:
    print(f"Congratulations! Your file: {file} ran successfully. ✨ 🍰 ✨")


def get_actual_error(stderr: str) -> str:
    # Most part of the errors are just stack traceback calls.
    # We just need the actual error message.
    return stderr.split("\n")[-2].strip()


def launch_interface(result_links: List[Dict[str, str]]) -> None:
    Interface(result_links)


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
        # We keep `check=False` so that we can show the stackoverflow link to the users.
        # And we must not show the traceback calls to this process when the execution of
        # file fails.
        process = subprocess.run(
            terminal_command, stdout=PIPE, stderr=PIPE, encoding="UTF-8"
        )

        if process.returncode == 0:
            display_success_message(args.file)
            sys.exit()

        actual_error = get_actual_error(process.stderr)
        result_links = parse_and_get_results(actual_error)
        launch_interface(result_links)
    elif args.query is not None:
        result_links = parse_and_get_results(args.query)
        launch_interface(result_links)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

import subprocess
import sys
from subprocess import PIPE
from typing import Dict, List

from cli_output import Interface
from fetch_results import parse_and_get_results


def display_success_message(file: List[str]) -> None:
    file_name_with_path = " ".join(file)
    print(f"Congratulations! Your file: {file_name_with_path} ran successfully. ✨ 🍰 ✨")


def get_actual_error(stderr: str) -> str:
    # Most part of the errors are just stack traceback calls.
    # We just need the actual error message.
    return stderr.split("\n")[-2].strip()


def launch_interface(result_links: List[Dict[str, str]]) -> None:
    Interface(result_links)


def main() -> None:
    language = "python3"
    # We obtain a file with its path (if provided).
    file = sys.argv[1:]
    terminal_command = [language] + file
    # We keep `check=False` so that we can show the stackoverflow link to the users.
    # And we must not show the traceback calls to this process when the execution of
    # file fails.
    process = subprocess.run(
        terminal_command, stdout=PIPE, stderr=PIPE, encoding="UTF-8"
    )

    if process.returncode == 0:
        display_success_message(file)
        sys.exit()

    actual_error = get_actual_error(process.stderr)
    result_links = parse_and_get_results(actual_error)
    launch_interface(result_links)


if __name__ == "__main__":
    main()

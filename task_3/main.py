import sys
from pathlib import Path
from colorama import init, Fore


DIR_COLOR = Fore.BLUE
FILE_COLOR = Fore.GREEN
ERROR_COLOR = Fore.RED
WARNING_COLOR = Fore.YELLOW
INFO_COLOR = Fore.CYAN


def display_directory_structure(directory_path: Path, prefix: str = "") -> None:
    """
    Recursively displays the structure of a directory with colored output.
    - Directories are printed in blue.
    - Files are printed in green.
    - A PermissionError is handled by printing a red error message.
    """
    try:
        items = sorted(list(directory_path.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))
    except PermissionError:
        print(f"{prefix}{ERROR_COLOR}Permission denied to read: {directory_path.name}")
        return

    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "┗━━ " if is_last else "┣━━ "

        if item.is_dir():
            print(f"{prefix}{connector}{DIR_COLOR}{item.name}")
            new_prefix = prefix + ("    " if is_last else "┃   ")
            display_directory_structure(item, new_prefix)
        else:
            print(f"{prefix}{connector}{FILE_COLOR}{item.name}")


def main():
    """
    Entry point of the script.
    Validates the command-line argument and starts the directory traversal.
    """
    init(autoreset=True)

    if len(sys.argv) != 2:
        print(f"{ERROR_COLOR}Error: A directory path must be provided as an argument.")
        print(f"{WARNING_COLOR}Usage: python {sys.argv[0]} <path_to_directory>")
        sys.exit(1)

    target_path = Path(sys.argv[1])

    if not target_path.exists():
        print(f"{ERROR_COLOR}Error: Path '{target_path}' does not exist.")
        sys.exit(1)
    elif not target_path.is_dir():
        print(f"{ERROR_COLOR}Error: Path '{target_path}' is not a directory.")
        sys.exit(1)

    print(f"\n{INFO_COLOR}Displaying structure for: {target_path.resolve()}\n")
    display_directory_structure(target_path)


if __name__ == "__main__":
    main()

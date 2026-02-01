import os
import sys
from typing import Tuple


def total_salary(path: str) -> Tuple[int, int]:
    """
    Analyzes a salary file and returns the total and average salary.

    This function reads a text file where each line contains a developer's
    name and their salary, separated by a comma. It calculates the
    sum of all salaries and the average salary.

    Args:
        path (str): The path to the text file with salaries.

    Returns:
        Tuple[int, int]: A tuple containing two integers:
                         - The total sum of all salaries.
                         - The average salary.
                         Returns (0, 0) if the file is empty,
                         or contains no valid salary data.

    Doctests:
    Note: These tests create and remove files, which can leave artifacts if
    tests fail unexpectedly. For more complex applications, using a dedicated
    testing framework like pytest with fixtures for file handling is recommended.

    >>> # Create a test file with valid data
    >>> with open("test_salaries.txt", "w", encoding="utf-8") as f:
    ...     _ = f.write("Alex Korp,3000\\n")
    ...     _ = f.write("Nikita Borisenko,2000\\n")
    ...     _ = f.write("Sitarama Raju,1000\\n")
    >>> total_salary("test_salaries.txt")
    (6000, 2000)
    >>> os.remove("test_salaries.txt")

    >>> # Test with an empty file
    >>> with open("empty_salaries.txt", "w", encoding="utf-8") as f:
    ...     pass
    >>> total_salary("empty_salaries.txt")
    (0, 0)
    >>> os.remove("empty_salaries.txt")

    >>> # Test with a non-existent file
    >>> total_salary("non_existent_file.txt") # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    FileNotFoundError: [Errno 2] No such file or directory: 'non_existent_file.txt'

    >>> # Test with malformed lines
    >>> with open("malformed_salaries.txt", "w", encoding="utf-8") as f:
    ...     _ = f.write("Alex Korp,3000\\n")
    ...     _ = f.write("Invalid Line\\n")
    ...     _ = f.write("John Doe,abcd\\n")
    ...     _ = f.write(",5000\\n")
    >>> total_salary("malformed_salaries.txt")
    Warning: Skipping malformed line: Invalid Line
    Warning: Skipping malformed line: John Doe,abcd
    Warning: Skipping malformed line: ,5000
    (3000, 3000)
    >>> os.remove("malformed_salaries.txt")

    >>> # Test with only malformed lines
    >>> with open("all_malformed.txt", "w", encoding="utf-8") as f:
    ...     _ = f.write("Invalid Line 1\\n")
    ...     _ = f.write("Invalid Line 2\\n")
    >>> total_salary("all_malformed.txt")
    Warning: Skipping malformed line: Invalid Line 1
    Warning: Skipping malformed line: Invalid Line 2
    (0, 0)
    >>> os.remove("all_malformed.txt")
    """
    total = 0
    count = 0
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                parts = line.split(",")
                if len(parts) != 2 or not parts[0] or not parts[1]:
                    raise ValueError("Line format is incorrect.")
                salary = int(parts[1])
                total += salary
                count += 1
            except ValueError:
                print(f"Warning: Skipping malformed line: {line}")
                continue

    if count == 0:
        return (0, 0)

    average = total / count
    return (total, int(average))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    default_file = "salary_file.txt"

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = default_file
        print(f"No file path provided. Using dummy data in '{path}'.")
        with open(path, "w", encoding="utf-8") as f:
            f.write("Alex Korp,3000\n")
            f.write("Nikita Borisenko,2000\n")
            f.write("Sitarama Raju,1000\n")

    try:
        total, average = total_salary(path)
        print(f"Total salary: {total}, Average salary: {average}")
    except FileNotFoundError:
        print(f"Error: The file at '{path}' was not found.")
    finally:
        if path == default_file and os.path.exists(path):
            os.remove(path)

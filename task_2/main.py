from pathlib import Path

def get_cats_info(path: str | Path) -> list[dict]:
    """
    Reads a file with cat information and returns a list of dictionaries.

    Each line in the file should contain a unique cat ID, name, and age,
    separated by a comma.

    Args:
        path: The path to the text file.

    Returns:
        A list of dictionaries, where each dictionary contains information
        about one cat (id, name, age). Returns an empty list if the file
        is not found or an error occurs.
    """
    cats_info = []

    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) == 3:
                    cat_id, name, age = parts
                    cats_info.append({
                        "id": cat_id,
                        "name": name,
                        "age": age
                    })
    except FileNotFoundError:
        return []

    return cats_info

if __name__ == "__main__":
    file_path = Path("cats_example.txt")
    try:
        file_path.write_text(
            "60b90c1c13067a15887e1ae1,Tayson,3\n"
            "60b90c2413067a15887e1ae2,Vika,1\n"
            "malformed-line\n"
        )

        cats = get_cats_info(file_path)
        print(cats)

    finally:
        if file_path.exists():
            file_path.unlink()

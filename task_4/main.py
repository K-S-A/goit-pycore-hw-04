from functools import wraps


def validate_args(expected_count: int, usage: str):
    def decorator(func):
        @wraps(func)
        def wrapper(args, *func_args):
            if len(args) != expected_count:
                return f"Invalid arguments. Usage: {usage}"
            return func(args, *func_args)
        return wrapper
    return decorator


def parse_input(user_input) -> tuple[str, list]:
    """
    Parses user input into a command and its arguments.

    >>> parse_input("hello")
    ('hello', [])
    >>> parse_input("add John 1234567890")
    ('add', ['John', '1234567890'])
    >>> parse_input("  ALL ")
    ('all', [])
    """
    parts = user_input.split()
    if not parts:
        return "", []

    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


@validate_args(2, "add [name] [phone]")
def add_contact(args, contacts) -> str:
    """
    Adds a contact to the contacts dictionary.
    Returns a confirmation message.

    >>> contacts = {}
    >>> add_contact(["John", "12345"], contacts)
    'Contact added.'
    >>> contacts
    {'John': '12345'}
    >>> add_contact(["John", "54321"], contacts) # Test overwrite
    'Contact added.'
    >>> contacts
    {'John': '54321'}
    >>> add_contact(["Jane"], contacts)
    'Invalid arguments. Usage: add [name] [phone]'
    """
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@validate_args(2, "change [name] [new_phone]")
def change_contact(args, contacts) -> str:
    """
    Changes the phone number for an existing contact.
    Returns a confirmation or error message.

    >>> contacts = {"John": "12345"}
    >>> change_contact(["John", "54321"], contacts)
    'Contact updated.'
    >>> contacts
    {'John': '54321'}
    >>> change_contact(["Jane", "98765"], contacts)
    'Contact not found.'
    >>> change_contact(["John"], contacts)
    'Invalid arguments. Usage: change [name] [new_phone]'
    """
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return "Contact updated."
    else:
        return "Contact not found."


@validate_args(1, "phone [name]")
def show_phone(args, contacts) -> str:
    """
    Retrieves the phone number for a contact.
    Returns the phone number or an error message.

    >>> contacts = {"John": "12345"}
    >>> show_phone(["John"], contacts)
    '12345'
    >>> show_phone(["Jane"], contacts)
    'Contact not found.'
    >>> show_phone([], contacts)
    'Invalid arguments. Usage: phone [name]'
    """
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        return "Contact not found."


def show_all(contacts) -> str:
    """
    Shows all contacts in the dictionary.
    Returns a formatted string of all contacts or a message if empty.

    >>> contacts = {"John": "12345", "Jane": "54321"}
    >>> print(show_all(contacts))
    John: 12345
    Jane: 54321
    >>> show_all({})
    'No contacts found.'
    """
    if not contacts:
        return "No contacts found."

    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])


def main():
    """
    Main function to run the assistant bot.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    main()
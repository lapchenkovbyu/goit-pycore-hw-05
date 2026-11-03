"""Task 4: console assistant bot with error handling via a decorator."""

from typing import Callable

ARGS_ERROR = "Enter the argument for the command"
NOT_FOUND_ERROR = "Contact not found."


def input_error(func: Callable[..., str]) -> Callable[..., str]:
    """Catch input errors of a command handler and return a user message."""

    def inner(*args, **kwargs) -> str:
        try:
            return func(*args, **kwargs)
        except KeyError:
            return NOT_FOUND_ERROR
        except (ValueError, IndexError):
            return ARGS_ERROR

    return inner


def parse_input(user_input: str) -> tuple[str, ...]:
    """Split input into a lowercase command and its arguments."""
    parts = user_input.split()
    if not parts:
        return ("",)
    cmd, *args = parts
    return cmd.strip().lower(), *args


def _find_name(name: str, contacts: dict[str, str]) -> str:
    """Return the stored key matching `name` case-insensitively.

    Raises KeyError if there is no such contact.
    """
    for stored_name in contacts:
        if stored_name.lower() == name.lower():
            return stored_name
    raise KeyError(name)


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """add [name] [phone]: save a contact (overwrites an existing one)."""
    name, phone = args  # ValueError if not exactly two arguments
    try:
        name = _find_name(name, contacts)
    except KeyError:
        pass  # new contact: keep the name as typed
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """change [name] [new phone]: update the phone of an existing contact."""
    name, phone = args
    contacts[_find_name(name, contacts)] = phone  # KeyError if missing
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """phone [name]: return the phone of a contact."""
    return contacts[_find_name(args[0], contacts)]  # IndexError / KeyError


@input_error
def show_all(contacts: dict[str, str]) -> str:
    """all: return every saved contact, one per line."""
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main() -> None:
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

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
    main()

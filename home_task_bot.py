import re
import os
from home_task_abook import Record
from home_task_abook import AddressBook

INVALID_PHONE = "Inavlid phone number! " \
    "Enter the phone number in the format 10 digits"
INVALID_ARGUMENTS = "Enter the argument for the command."
KEY_ERROR = "Record is missing!"
INVALID_COMMAND = "Enter valid command."


class ValidPhoneError(Exception):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return INVALID_ARGUMENTS
        except KeyError:
            return KEY_ERROR
        except ValidPhoneError:
            return INVALID_PHONE
        except ValueError as e:
            return str(e)
    return inner


def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def validate_phone_number(value: str) -> str:
    phone_number = re.match(r"^\d{10}$", value) if value is not None else None
    return None if phone_number is None else phone_number.group(0)


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    name = args[0]
    phone = None if len(args)<2 else args[1]
    
    name = name.capitalize()
    record = book.find(name)

    message = f"Contact {name} updated."
    if  record is None:
        record = Record(name)
        book.add_record(record)
        message = f"Contact {name} added."
    
    if phone is not None:
        phone = validate_phone_number(phone)
        if phone is None:
            raise ValidPhoneError(INVALID_PHONE)
        record.add_phone(phone)

    return message


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    name = args[0]

    name = name.capitalize()
    record = book.find(name)
    if record is None:
        return add_contact(args, book)

    old_phone = args[1] if len(args)>=2 else None
    new_phone = args[2] if len(args)>=3 else None
    
    old_phone = validate_phone_number(old_phone)
    new_phone = validate_phone_number(new_phone)
    if old_phone is None or new_phone is None:
        raise ValidPhoneError(INVALID_PHONE)

    return record.edit_phone(old_phone, new_phone)+f" for {name}."
     

@input_error
def get_phone_by_name(args: list, book: AddressBook) -> str:
    name = args[0]
    name = name.capitalize()

    record = book.find(name)
    if record is None:
        return KEY_ERROR
    
    return list(map(lambda phone: phone.value,record.phones)) 

@input_error
def add_birthday(args: list, book: AddressBook):
    name = args[0]
    bday = None if len(args)<2 else args[1]
    
    name = name.capitalize()
    record = book.find(name)

    if record is None:
        return KEY_ERROR
    
    if bday is not None:
        record.add_birthday(bday)
        
    message = f"Birthday {record.birthday.value} successfully added for {record.name.value} "
    if record.birthday is None:
        message = f"Invalid birthday format. Use DD.MM.YYYY. "

    return message

@input_error
def show_birthday(args: list, book: AddressBook)-> str:
    name = args[0]
    name = name.capitalize()

    record = book.find(name)
    if record is None:
        return KEY_ERROR
    
    return record.birthday if record.birthday is not None else "Birthday record absent."

@input_error
def birthdays(args: list, book: AddressBook)->str:
    return book.get_upcoming_birthdays()

def get_all_contacts(args: list, book: AddressBook) -> str:
    return f"{book}"


def main():
    book = AddressBook()

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
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone_by_name(args, book))
        elif command == "all":
            print(get_all_contacts(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "clear":
            clear_console()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

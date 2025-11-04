from collections import UserDict
import re
import datetime

class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone: str):
        phone_number = re.match(r"^\d{10}$", phone)

        if phone_number is None:
            raise ValueError("Введіть телефон в форматі 10 чисел")
            return
        
        self.__value = phone_number.group(0)

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.datetime = datetime.strptime(value,"DD.MM.YYYY")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        

class Record:

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str):
        try:
            phone = Phone(phone_number)

            if phone.value not in [p.value for p in self.phones]:
                self.phones.append(phone)

        except ValueError as e:
            pass

    def add_birthday(self, value: str):
        try:
            self.birthday = Birthday(str)
        except ValueError as e:
            self.birthday = None
            print(e)
    
    def remove_phone(self, phone_number: str):
        phone_to_remove = self.find_phone(phone_number)

        if phone_to_remove:
            self.__phones.remove(phone_to_remove)

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        phone_to_edit = self.find_phone(old_phone_number)
        if not phone_to_edit:
            return f"Phone number {old_phone_number} absent"

        try:
            if phone_to_edit.value == new_phone_number:
                return f"You have enter the same phones {old_phone_number} and {new_phone_number}"

            phone_to_edit.value = new_phone_number
            return f"Phone {old_phone_number} updated to {new_phone_number}"
        except ValueError as e:
            return f"Edit error" # print(f"Помилка при редагуванні: {e}")

    def find_phone(self, phone_number: str) -> Phone | None:
        iterator = filter(lambda phone: phone.value == phone_number, self.phones)
        return next(iterator, None)

    def __str__(self)-> str:
        phones_str = ", ".join("'"+p.value+"'" for p in self.phones)
        return f"Contact: {self.name.value}, Phones: {"["+phones_str+"]" if phones_str else 'Empty list'}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        name_key = record.name.value

        if name_key in self.data:
            pass # print(f"Контакт {name_key} вже існує. Для оновлення використовуйте редагування.")
        else:
            self.data[name_key] = record
            # print(f"Контакт {name_key} успішно додано.")

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            # print(f"Контакт {name} видалено.")
        else:
            pass # print(f"Контакт {name} не знайдено.")

    def get_upcoming_birthdays(self)->list:
        result = []
        return result

    def __str__(self):
        if not self.data:
            return "Adress book is empty."

        return "\n".join(str(record) for record in self.data.values())

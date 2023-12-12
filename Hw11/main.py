from collections import UserDict
from datetime import datetime
import re
import pickle


class Field:
    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, user_name):
        if type(user_name) is str:
            self.__value = user_name
        else:
            raise ValueError(f'User name should be string type')


class Birthday(Field):
    pattern = r"\d{2}\.\d{2}\.\d{4}"
    def __init__(self, value):
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday_date):
        if birthday_date is None:
            self.__value = birthday_date
        elif re.fullmatch(self.pattern, birthday_date):
            self.__value = birthday_date
        else:
            raise ValueError(f'Birthday date is invalid')


class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if phone.isdigit() and (len(phone) == 12 if phone.startswith("380") else len(phone) == 10):
            self.__value = phone
        else:
            raise ValueError(f"Phone number is not correct")

    def __str__(self):
        return self.value


class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        if phone.value not in [p.value for p in self.phones]:
            # print(phone)
            self.phones.append(phone)

    def remove_phone(self, phone_value):
        phone = Phone(phone_value)
        if phone.value not in [p.value for p in self.phones]:
            raise ValueError(f"Phone is not in list")
        else:
            index = [p.value for p in self.phones].index(phone.value)
            del self.phones[index]

    def edit_phone(self, phone_old, phone_new):
        if Phone(phone_old).value not in [p.value for p in self.phones]:
            raise ValueError(f"Phone is not in list")

        for phone in self.phones:
            if phone.value == phone_old:
                phone.value = phone_new

    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone
        return None

    def day_to_birthday(self):
        if self.birthday is not None:
            current_date = datetime.now().date()
            birthday_date = datetime.strptime(self.birthday.value, '%d.%m.%Y').date()
            birthday_date = birthday_date.replace(year=current_date.year)  # Year changing to compare with current date
            if current_date > birthday_date:
                # If the birthday has already passed in this year, then the year should be changed for the next year
                birthday_date = birthday_date.replace(year=current_date.year+1)
                days_to_birthday = birthday_date - current_date
                return print(f'The birthday is in {days_to_birthday.days} days')
            elif current_date == birthday_date:
                return print(f'The birthday is TODAY!!!')
            else:
                days_to_birthday = birthday_date - current_date
                return print(f'The birthday is in {days_to_birthday.days} days')

    def __str__(self):
        return (f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}" +
                (f', birthday date: {self.birthday.value}' if self.birthday.value is not None else f''))


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: Name):
        return self.data.get(name)

    def iterator(self, quantity_of_records):
        start_point = 0
        while start_point < len(self.data):
            new_list = []
            for i, v in enumerate(self.data.values()):
                if start_point <= i < (start_point+quantity_of_records):
                    new_list.append(v)
            yield new_list
            start_point += quantity_of_records

    def save_to_file(self):
        with open("addressbook.bin", "wb") as f:
            pickle.dump(self.data, f)

    def load_from_file(self, file):
        with open(file, "rb") as f:
            self.data = pickle.load(f)

    def search(self, data_to_find: str):
        print("Search result:")
        search_result = []
        for val in self.data.values():
            if (data_to_find.lower() in str(val.name).lower()
                    or any(data_to_find in str(phone) for phone in val.phones)):
                search_result.append(str(val))

        for i in search_result:
            print(i)

    def delete(self, name: Name):
        for key, value in self.data.items():
            if key == name:
                return self.data.pop(name)
        return f"Contact name: {name} was not found in AddressBook"

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John", "30.12.2005")
john_record.add_phone("0234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Створення та додавання нового запису для Tom
tom_record = Record("Tom")
tom_record.add_phone("1234657623")
book.add_record(tom_record)

# Створення та додавання нового запису для Kate
kate_record = Record("Kate")
kate_record.add_phone("1234657623")
book.add_record(kate_record)

# Створення та додавання нового запису для Carl
carl_record = Record("Kate")
carl_record.add_phone("1234657623")
book.add_record(carl_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

john_record.day_to_birthday()

# Знаходження та редагування телефону для John
john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
# print(f"{john.name} found: {found_phone}")  # Виведення: 5555555555

# iterator = book.iterator(2)
# print(next(iterator))

book.save_to_file()

print("book recorded")

# Видалення запису Jane
book.delete("Jane")
book.delete("John")

print("book deleted")

for name, record in book.data.items():
    print(record)

book.load_from_file("addressbook.bin")

print("book loaded")

for name, record in book.data.items():
    print(record)

print("jik")

book.search("1")

book.search("5")
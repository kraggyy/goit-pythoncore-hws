from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value) -> None:
        self.__value = None
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone):
        if phone.isdigit() and len(phone) == 10:
            self.__value = phone
        else:
            raise ValueError(f"Phone number is not correct")

    def __str__(self):
        return self.value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        if phone.value not in [p.value for p in self.phones]:
            print(phone)
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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: Name):
        return self.data.get(name)

    def delete(self, name: Name):
        for key, value in self.data.items():
            if key == name:
                return self.data.pop(name)
        return f"Contact name: {name} was not found in AddressBook"
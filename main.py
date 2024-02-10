import re
from pprint import pprint
import csv

# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for contact in contacts_list[1:]:
    fullname = re.split(r'\s+', contact[0])

    if len(fullname) == 3:
        contact[0] = f"{fullname[0]} {fullname[1]} {fullname[2]}"
        contact[1] = fullname[0]
        contact[2] = fullname[1]
        contact.insert(3, fullname[2])
    elif len(fullname) == 2:
        contact[0] = f"{fullname[0]} {fullname[1]}"
        contact[1] = fullname[0]
        contact[2] = fullname[1]

    phone = re.sub(r'(\+?[78])?[\s\(\-\)–]*([^\s\(\)\-–]{3})[\s\(\)\-–]*([^\s\(\)\-–]{3})[\s\(\)\-–]*([^\s\(\)\-–]{2})[\s\(\)\-–]*([^\s\(\)\-–]{2})\s*(?:\(?(доб\.)\s*(\d+)\)?)?', r'+7(\2)\3-\4-\5 \6\7', contact[5])
    contact[5] = phone

unique_contacts = {}
for contact in contacts_list[1:]:
    fullname = contact[1] + ' ' + contact[2]
    if fullname not in unique_contacts:
        unique_contacts[fullname] = contact
    else:
        for index, value in enumerate(contact):
            if value != unique_contacts[fullname][index]:
                if value and not unique_contacts[fullname][index]:
                    unique_contacts[fullname][index] = value

# Преобразование словаря обратно в список
result = [["ФИО", "Имя", "Фамилия", "Отчество", "Должность", "Телефон"]] + list(unique_contacts.values())

# Сохранение данных в другой файл (пункт 4)
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)

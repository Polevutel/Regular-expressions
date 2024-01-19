import csv
import re

def format_phone_number(phone_number):
    return re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\1\2)-\3-\4-\5', phone_number)

def merge_duplicate_contacts(contacts_list):
    merged_contacts = {}
    for contact in contacts_list:
        key = (contact[0], contact[1], contact[3])
        if key in merged_contacts:
            # merge the contact details
            merged_contact = merged_contacts[key]
            for i in range(5, len(contact)):
                if not merged_contact[i] and contact[i]:
                    merged_contact[i] = contact[i]
        else:
            merged_contacts[key] = contact
    return list(merged_contacts.values())

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    # Removing header from the list
    header = contacts_list.pop(0)

# Split full names and format phone numbers
for contact in contacts_list:
    full_name = contact[0].split()
    if len(full_name) < 2:
        continue
    first_name = full_name[0]
    last_name = full_name[1]
    middle_name = full_name[2] if len(full_name) > 2 else ''
    contact[0] = last_name
    contact.insert(0, first_name)
    contact.insert(2, middle_name)
    contact[5] = format_phone_number(contact[5])
    del contact[6:]  # Remove extra data if present

# Merge duplicate contacts
contacts_list = merge_duplicate_contacts(contacts_list)

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f)
    datawriter.writerow(header)
    datawriter.writerows(contacts_list)

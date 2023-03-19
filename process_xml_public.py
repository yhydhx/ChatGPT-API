from bs4 import BeautifulSoup
import os
from statistics import mean

def words_in_string(word_list, a_string):
    return set(word_list).intersection(a_string.split())

rewrite_directory = ''
original_directory = ''

list_of_files_to_check = []
list_of_anonymized_reports = []

for filename in os.listdir(rewrite_directory):
    f = os.path.join(rewrite_directory, filename)
    if os.path.isfile(f):
        target_file = os.path.basename(os.path.normpath(f))[:-15]
        print(target_file)
        list_of_files_to_check.append(target_file)

        text_file = open(f, "r")
        data = text_file.read()
        list_of_anonymized_reports.append(data)
        text_file.close()

print(list_of_files_to_check)
print(list_of_anonymized_reports)

list_of_accuracies = []
for i in range(len(list_of_files_to_check)):
    names = []
    professions = []
    locations = []
    ages = []
    dates = []
    contacts = []
    ids = []

    names_count = 0
    professions_count = 0
    locations_count = 0
    ages_count = 0
    dates_count = 0
    contacts_count = 0
    ids_count = 0

    with open(original_directory + "/" + list_of_files_to_check[i] + ".xml") as fp:
        soup = BeautifulSoup(fp, features="xml")
        text = soup.find('TEXT')
        text_content = text.contents[0]

        tags = soup.find("TAGS")

        name_tags = tags.find_all('NAME')
        for name_tag in name_tags:
            names.append(name_tag.get('text'))

        profession_tags = tags.find_all('PROFESSION')
        for profession_tag in profession_tags:
            professions.append(profession_tag.get('text'))

        location_tags = tags.find_all('LOCATION')
        for location_tag in location_tags:
            locations.append(location_tag.get('text'))

        age_tags = tags.find_all('AGE')
        for age_tag in age_tags:
            ages.append(age_tag.get('text'))

        date_tags = tags.find_all('DATE')
        for date_tag in date_tags:
            dates.append(date_tag.get('text'))

        contact_tags = tags.find_all('CONTACT')
        for contact_tag in contact_tags:
            contacts.append(contact_tag.get('text'))

        id_tags = tags.find_all('ID')
        for id_tag in id_tags:
            ids.append(id_tag.get('text'))

    print("==========================")
    print(list_of_files_to_check[i])
    a_string = list_of_anonymized_reports[i]

    print("Names: ", names)
    for word in words_in_string(names, a_string):
        names_count += 1

    print("Professions: ", professions)
    for word in words_in_string(professions, a_string):
        professions_count += 1

    print("Locations: ", locations)
    for word in words_in_string(locations, a_string):
        locations_count += 1

    print("Ages: ", ages)
    for word in words_in_string(ages, a_string):
        ages_count += 1

    print("Dates: ", dates)
    for word in words_in_string(dates, a_string):
        dates_count += 1

    print("Contacts: ", contacts)
    for word in words_in_string(contacts, a_string):
        contacts_count += 1

    print("IDs: ", ids)
    for word in words_in_string(ids, a_string):
        ids_count += 1

    print("Names remaining: ", names_count)
    print("Professions remaining: ", professions_count)
    print("Locations remaining: ", locations_count)
    print("Ages remaining: ", ages_count)
    print("Dates remaining: ", dates_count)
    print("Contacts remaining: ", contacts_count)
    print("Ids remaining: ", ids_count)

    sum = names_count + professions_count + locations_count + ages_count +  dates_count + contacts_count + ids_count
    total_length = len(names) + len(professions) + len(locations) + len(ages) + len(dates) + len(contacts) + len(ids)
    print("Remaining number of strings and Accuracy: ", sum, 1 - (sum/total_length))

    list_of_accuracies.append(1 - (sum/total_length))
    print("==========================\n")


print(len(list_of_files_to_check))
print("Average accuracy =", round(mean(list_of_accuracies), 3))


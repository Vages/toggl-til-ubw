#!/usr/local/bin/python3
import csv
from collections import defaultdict
from time_helpers import add_two_durations, get_all_dates_in_range_inclusive, round_duration_to_nearest_half_hour, \
    convert_duration_to_hour_number
import re

DESCRIPTION = 'description'
START_DATE = 'start_date'
DURATION = 'duration'
TAGS = 'tags'

ZERO_DURATION = "00:00:00"


def load_the_file_and_read_relevant_information(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [{
            DESCRIPTION: row['Description'],
            START_DATE: row['Start date'],
            DURATION: row['Duration'],
            TAGS: row['Tags']
        } for row in csv_reader]


def add_all_durations_for_a_list_of_entries(entries):
    combined_duration = ZERO_DURATION

    for entry in entries:
        combined_duration = add_two_durations(combined_duration, entry[DURATION])

    return combined_duration


def extract_activity_name_from_string(some_string):
    try:
        return some_string.split("aktivitet:")[1]
    except IndexError:
        return


def extract_time_code_from_string(some_string):
    time_code_regex = re.compile('timekode:([0-9\-]*)')
    search_result = time_code_regex.search(some_string)
    if search_result:
        return search_result.group(1)


def split_tags(tag_list):
    return tag_list.split(',')


def get_activity_name_from_entry(entry):
    the_tags = split_tags(entry[TAGS])

    for tag in the_tags:
        activity_name = extract_activity_name_from_string(tag)
        if activity_name:
            return activity_name

    return ""


def get_time_code_from_entry(entry):
    the_tags = split_tags(entry[TAGS])

    for tag in the_tags:
        time_code = extract_time_code_from_string(tag)
        if time_code:
            return time_code

    return ""


def get_description_from_entry(entry):
    return entry[DESCRIPTION]


def get_start_date_from_entry(entry):
    return entry[START_DATE]


def group_entries_as_they_should_be(all_entries):
    grouped = defaultdict(list)
    fingerprints_ignoring_start_dates = set()

    for entry in all_entries:
        fingerprint = (
            get_time_code_from_entry(entry),
            get_activity_name_from_entry(entry),
            get_description_from_entry(entry),
            get_start_date_from_entry(entry),
        )

        fingerprints_ignoring_start_dates.add(fingerprint[:-1])

        grouped[fingerprint].append(entry)

    grouped_and_combined = defaultdict(lambda: ZERO_DURATION)

    for fingerprint in grouped:
        the_entries = grouped[fingerprint]

        combined_duration = add_all_durations_for_a_list_of_entries(the_entries)

        grouped_and_combined[fingerprint] = combined_duration

    first_date = get_start_date_from_entry(min(all_entries, key=get_start_date_from_entry))
    last_date = get_start_date_from_entry(max(all_entries, key=get_start_date_from_entry))

    all_dates = get_all_dates_in_range_inclusive(first_date, last_date)

    the_main_table = []
    for fp in sorted(list(fingerprints_ignoring_start_dates)):
        the_row = [item.strip() for item in fp]

        for date in all_dates:
            lol = convert_duration_to_hour_number(
                round_duration_to_nearest_half_hour(grouped_and_combined[fp + (date, )]))

            the_row.append(str(lol))

        the_main_table.append(the_row)
    return the_main_table


def convert_toggl_report_to_python_array(file_path):
    time_entries = load_the_file_and_read_relevant_information(file_path)

    return group_entries_as_they_should_be(time_entries)


def two_d_array_to_csv(two_d_array):
    string_rows = []
    for row in two_d_array:
        string_rows.append(",".join(row))

    return "\n".join(string_rows)


if __name__ == '__main__':
    import fileinput

    for file_path in fileinput.input():
        print(two_d_array_to_csv(convert_toggl_report_to_python_array(file_path)))

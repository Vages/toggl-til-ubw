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


def load_the_file_and_read_relevant_information(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [{
            DESCRIPTION: row['Description'],
            START_DATE: row['Start date'],
            DURATION: row['Duration'],
            TAGS: row['Tags']
        } for row in csv_reader]


def group_time_entries_by_description(time_entries):
    items_by_description = defaultdict(list)
    for entry in time_entries:
        items_by_description[entry[DESCRIPTION]].append(entry)
    return dict(items_by_description)


def group_time_entries_by_start_date(time_entries):
    items_by_start_date = defaultdict(list)
    for entry in time_entries:
        items_by_start_date[entry[START_DATE]].append(entry)
    return dict(items_by_start_date)


def combine_all_entries_from_one_day_sharing_same_description(entries):
    """
    We assume that the entries have already been grouped by day and description
    """
    combined_duration = "00:00:00"

    for entry in entries:
        combined_duration = add_two_durations(combined_duration, entry[DURATION])

    arbitrary_entry = entries[0]
    return {
        DESCRIPTION: arbitrary_entry[DESCRIPTION],
        START_DATE: arbitrary_entry[START_DATE],
        DURATION: combined_duration,
        TAGS: arbitrary_entry[TAGS]
    }


def get_hours_worked_on_task_on_a_given_day(all_entries, task_description, day):
    by_description = group_time_entries_by_description(all_entries)
    relevant_entries = by_description[task_description]
    by_start_date = group_time_entries_by_start_date(relevant_entries)
    try:
        index_of_first_item_because_it_should_be_the_only_item = 0
        duration_as_string = by_start_date[day][index_of_first_item_because_it_should_be_the_only_item][DURATION]
        return convert_duration_to_hour_number(round_duration_to_nearest_half_hour(duration_as_string))
    except KeyError:
        return 0


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


def convert_toggl_report_to_python_array(file_path):
    time_entries = load_the_file_and_read_relevant_information(file_path)
    by_description = group_time_entries_by_description(time_entries)
    all_descriptions = list(by_description.keys())
    combined_entries = []

    # There is an assumption here that something with the same description does not have different activities.
    # Or that they have a description at all!
    # But they may. We should group by some tuple here instead.
    # TODO: Change the grouping mechanism
    for group in by_description:
        by_start_date = group_time_entries_by_start_date(by_description[group])

        for inner_group in by_start_date:
            combined_entries.append(
                combine_all_entries_from_one_day_sharing_same_description(by_start_date[inner_group]))
    all_dates_with_time_entries_sorted = list(sorted(list(group_time_entries_by_start_date(combined_entries).keys())))
    first_date, last_date = all_dates_with_time_entries_sorted[0], all_dates_with_time_entries_sorted[-1]
    all_dates_in_range = get_all_dates_in_range_inclusive(first_date, last_date)
    the_main_table = []
    for description in all_descriptions:
        index_of_first_item_because_it_is_as_good_as_any = 0
        first_entry = by_description[description][index_of_first_item_because_it_is_as_good_as_any]
        the_time_code = get_time_code_from_entry(first_entry)
        the_activity_name = get_activity_name_from_entry(first_entry)

        the_row = [the_time_code, the_activity_name.strip(), description.strip()]

        for day in all_dates_in_range:
            the_row.append(str(get_hours_worked_on_task_on_a_given_day(combined_entries, description, day)))

        the_main_table.append(the_row)
    return list(sorted(the_main_table))


def two_d_array_to_csv(two_d_array):
    string_rows = []
    for row in two_d_array:
        string_rows.append(",".join(row))

    return "\n".join(string_rows)


if __name__ == '__main__':
    import fileinput

    for file_path in fileinput.input():
        print(two_d_array_to_csv(convert_toggl_report_to_python_array(file_path)))

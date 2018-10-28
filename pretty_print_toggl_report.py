#!/usr/local/bin/python3
from convert_toggl_report import convert_toggl_report_to_python_array


def create_table_from_two_d_array(two_d_array):
    first_row = two_d_array[0]

    maxes = [0] * len(first_row)
    sums = [0] * len(first_row)
    column_where_the_hour_numbers_start = 4

    for row in two_d_array:
        for i, item in enumerate(row):
            maxes[i] = max(maxes[i], len(item))
            if i >= column_where_the_hour_numbers_start:
                sums[i] += float(item)

    for i, a_sum in enumerate(sums):
        maxes[i] = max(maxes[i], len(str(a_sum)))

    string_converted_rows = []
    for row in two_d_array + [sums]:
        padded_items = []
        for i, item in enumerate(row):

            if item in ['0', 0]:
                the_item_to_display = ''
            elif i >= column_where_the_hour_numbers_start:
                the_item_to_display = str(float(item))
            else:
                the_item_to_display = item

            padded_items.append(the_item_to_display.ljust(maxes[i]))
        string_converted_rows.append(" | ".join(padded_items))

    with_empty_line_inserted = string_converted_rows[:-1] + [""] + string_converted_rows[-1:] + [
        "SUM: " + str(sum(sums))
    ]

    return '\n'.join(with_empty_line_inserted)


if __name__ == '__main__':
    import fileinput

    for file_path in fileinput.input():
        my_x = create_table_from_two_d_array(convert_toggl_report_to_python_array(file_path))

        print(my_x)

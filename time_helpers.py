import decimal
from datetime import time, datetime, date, timedelta

decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def convert_iso_string_to_time_delta(iso_string: str):
    """
    Inspired by https://stackoverflow.com/questions/35241643/convert-datetime-time-into-datetime-timedelta-in-python-3-4
    """
    string_as_time = time.fromisoformat(iso_string)
    return datetime.combine(date.min, string_as_time) - datetime.min


def add_two_durations(duration_a: str, duration_b: str):
    # Format timedelta to string: https://stackoverflow.com/questions/538666/python-format-timedelta-to-string
    return str(convert_iso_string_to_time_delta(duration_a) + convert_iso_string_to_time_delta(duration_b)).zfill(8)


def round_duration_to_nearest_half_hour(some_duration: str):
    as_time_delta = convert_iso_string_to_time_delta(some_duration)
    seconds_as_decimal = decimal.Decimal(as_time_delta.seconds)
    seconds_in_half_an_hour = decimal.Decimal(1800)
    number_of_half_hours = seconds_as_decimal / seconds_in_half_an_hour
    number_of_half_hours_rounded = round(
        number_of_half_hours,
        # Turns out that setting 0 as the number of decimals was really important.
        # Otherwise, the decimal rounding did not work.
        0)
    and_back_to_time_delta = timedelta(seconds=int(number_of_half_hours_rounded * seconds_in_half_an_hour))

    return str(and_back_to_time_delta).zfill(8)


def get_all_dates_in_range_inclusive(start_date, end_date):
    iterator = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    step = timedelta(days=1)

    all_dates = []
    while iterator <= end:
        all_dates.append(str(iterator).split(' ')[0])  # Take only the date portion
        iterator += step

    return all_dates


def convert_duration_to_hour_number(duration):
    total_seconds = decimal.Decimal(convert_iso_string_to_time_delta(duration).seconds)
    seconds_in_an_hour = decimal.Decimal(3600)
    hours = total_seconds / seconds_in_an_hour
    if hours % 1:
        return float(hours)
    return int(hours)

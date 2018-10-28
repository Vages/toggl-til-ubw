from unittest import TestCase
from time_helpers import add_two_durations, round_duration_to_nearest_half_hour, get_all_dates_in_range_inclusive, \
    convert_duration_to_hour_number


class TestTimeHelpers(TestCase):
    def test_add_two_durations(self):
        self.assertEqual('00:00:00', add_two_durations('00:00:00', '00:00:00'))
        self.assertEqual('00:00:34', add_two_durations('00:00:34', '00:00:00'))
        self.assertEqual('00:01:08', add_two_durations('00:00:34', '00:00:34'))
        self.assertEqual('23:09:07', add_two_durations('04:38:33', '18:30:34'))
        # Decided upon not testing for durations adding up to more than 24 hours, because we do not need that in UBW

    def test_round_duration_to_nearest_half_hour(self):
        self.assertEqual('00:00:00', round_duration_to_nearest_half_hour('00:00:00'))
        self.assertEqual('00:00:00', round_duration_to_nearest_half_hour('00:14:59'))
        self.assertEqual('00:30:00', round_duration_to_nearest_half_hour('00:15:00'))
        self.assertEqual('01:00:00', round_duration_to_nearest_half_hour('00:45:00'))
        self.assertEqual('00:30:00', round_duration_to_nearest_half_hour('00:44:59'))
        self.assertEqual('22:00:00', round_duration_to_nearest_half_hour('22:00:00'))
        self.assertEqual('22:00:00', round_duration_to_nearest_half_hour('22:14:59'))
        self.assertEqual('22:30:00', round_duration_to_nearest_half_hour('22:15:00'))
        self.assertEqual('23:00:00', round_duration_to_nearest_half_hour('22:45:00'))
        self.assertEqual('22:30:00', round_duration_to_nearest_half_hour('22:44:59'))

    def test_get_all_dates_in_range_inclusive(self):
        self.assertEqual([
            "2011-05-03", "2011-05-04", "2011-05-05", "2011-05-06", "2011-05-07", "2011-05-08", "2011-05-09",
            "2011-05-10"
        ], get_all_dates_in_range_inclusive('2011-05-03', "2011-05-10"))

    def test_convert_duration_to_hour_number(self):
        self.assertEqual(0, convert_duration_to_hour_number('00:00:00'))
        self.assertEqual(0.25, convert_duration_to_hour_number('00:15:00'))
        self.assertEqual(0.5, convert_duration_to_hour_number('00:30:00'))
        self.assertEqual(0.75, convert_duration_to_hour_number('00:45:00'))
        self.assertEqual(1, convert_duration_to_hour_number('01:00:00'))
        self.assertEqual(1.5, convert_duration_to_hour_number('01:30:00'))

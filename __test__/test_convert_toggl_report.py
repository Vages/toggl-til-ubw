from unittest import TestCase
from convert_toggl_report import two_d_array_to_csv, convert_toggl_report_to_python_array, \
    extract_time_code_from_string, extract_activity_name_from_string

the_output = """32010000-7\t\tBandrigging til Halloween-fest\t0\t0\t0\t0\t4.5
32010005-31\t25\tJulekalenderoppgaver\t0\t0\t0\t0\t2.5
32010005-31\t26\tJulekalenderoppgaver\t0\t0\t0\t1.5\t0
32010054-3\t\tCAOS-1133 Legge inn en Spring Boot-app som kommuniserer med ekstern maskinvare\t8\t9\t0\t0\t0
32010054-3\t\tErfaringsoverføring\t0\t0.5\t7\t2.5\t2.5
32010054-3\t\tQA: CAOS-1130 Automatisk oppdatering av Electron app\t0\t0\t0\t3.5\t0
32010054-3\t\tQA: CAOS-1216 Vis info om produkter per delstrekning\t0\t0\t2.5\t0\t1.5
32010054-3\t\tQA: CAOS-1227 Prototyping av protokoll som kundesenterløsningen skal bruke til å slå opp kunde- og ordredetaljer automatisk\t0\t1\t0\t0\t0
ABSENCE\t\tLege, tannlege,fysioterapi besøk\t0\t0\t0\t0\t2.5"""


class TestConvertTogglReport(TestCase):
    def test_extract_time_code_from_string(self):
        self.assertEqual("32010054-3", extract_time_code_from_string("foo bar timekode:32010054-3"))
        self.assertEqual("32010054-3", extract_time_code_from_string("footimekode:32010054-3"))
        self.assertEqual("32010054", extract_time_code_from_string("foo timekode:32010054"))
        self.assertEqual(None, extract_time_code_from_string("foo bar"))
        self.assertEqual(None, extract_time_code_from_string("foo bar timekode"))
        self.assertEqual("ABSENCE", extract_time_code_from_string("foo ny timekode:ABSENCE"))

    def test_extract_activity_name_from_string(self):
        self.assertEqual("26", extract_activity_name_from_string("foo bar aktivitet:26"))
        self.assertEqual("25", extract_activity_name_from_string("foo bar aktivitet:25"))
        self.assertEqual("25", extract_activity_name_from_string("aktivitet:25"))
        self.assertEqual("Denne strengen har mellomrom",
                         extract_activity_name_from_string("aktivitet:Denne strengen har mellomrom"))
        self.assertEqual(None, extract_activity_name_from_string("Denne strengen har ingen aktivitet"))

    def test_the_big_convert_function(self):
        self.maxDiff = None
        self.assertEqual(
            the_output,
            two_d_array_to_csv(
                convert_toggl_report_to_python_array('./Toggl_time_entries_2018-10-08_to_2018-10-14.csv')))

from unittest import TestCase
from convert_toggl_report import two_d_array_to_csv, convert_toggl_report_to_python_array, \
    extract_time_code_from_string, extract_activity_name_from_string

the_output = """32010000-7,,Bandrigging til Halloween-fest,0,0,0,0,4.5
32010005-31,Deltakelse,Julekalenderoppgaver,0,0,0,1.5,0
32010054-3,,CAOS-1133 Legge inn en Spring Boot-app som kommuniserer med ekstern maskinvare,8,9,0,0,0
32010054-3,,Erfaringsoverføring,0,0.5,7,2.5,2.5
32010054-3,,QA: CAOS-1130 Automatisk oppdatering av Electron app,0,0,0,3.5,0
32010054-3,,QA: CAOS-1216 Vis info om produkter per delstrekning,0,0,2.5,0,1.5
32010054-3,,QA: CAOS-1227 Prototyping av protokoll som kundesenterløsningen skal bruke til å slå opp kunde- og ordredetaljer automatisk,0,1,0,0,0"""


class TestConvertTogglReport(TestCase):
    def test_extract_time_code_from_string(self):
        self.assertEqual("32010054-3", extract_time_code_from_string("foo bar timekode:32010054-3"))
        self.assertEqual("32010054-3", extract_time_code_from_string("foo timekode:32010054-3 bar"))
        self.assertEqual("32010054", extract_time_code_from_string("foo timekode:32010054 bar"))
        self.assertEqual(None, extract_time_code_from_string("foo bar"))
        self.assertEqual(None, extract_time_code_from_string("foo ny timekode bar"))

    def test_extract_time_code_from_string(self):
        self.assertEqual("Deltakelse", extract_activity_name_from_string("foo bar aktivitet:Deltakelse"))
        self.assertEqual("Ledelse/koordinering",
                         extract_activity_name_from_string("foo bar aktivitet:Ledelse/koordinering"))
        self.assertEqual("Ledelse/koordinering", extract_activity_name_from_string("aktivitet:Ledelse/koordinering"))
        self.assertEqual("Denne strengen har mellomrom",
                         extract_activity_name_from_string("aktivitet:Denne strengen har mellomrom"))
        self.assertEqual(None, extract_activity_name_from_string("Denne strengen har ingen aktivitet"))

    def test_the_big_convert_function(self):
        self.assertEqual(
            the_output,
            two_d_array_to_csv(
                convert_toggl_report_to_python_array('./Toggl_time_entries_2018-10-08_to_2018-10-14.csv')))

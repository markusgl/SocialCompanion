import datetime

from unittest import TestCase
from actions_core import ActionSearchAppointment
from datetime import timedelta

class TestActionSearchAppointment(TestCase):
    def setUp(self):
        self.asa = ActionSearchAppointment()

    def test_convert_relativedate(self):
        relativedate = 'heute'
        today = datetime.datetime.now()
        start_time, end_time = self.asa._convert_relativedate(relativedate)
        self.assertEqual(start_time, today)
        self.assertEqual(end_time, 0)

    def test_convert_dateperiod_next_days(self):
        dateperiod = 'nächsten Tage'
        today = datetime.datetime.now()
        start_time, end_time = self.asa._convert_dateperiod(dateperiod)
        self.assertEqual(start_time, today)
        self.assertEqual(end_time, 4)

    def test_search_google_calendar_by_time(self):
        start_time = datetime.datetime.now()
        self.asa._search_google_calendar_by_time(start_time, 2)

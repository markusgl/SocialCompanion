from google_calendar_tasks import GoogleCalendarTasks
from date_converter import DateConverter


def test_search_google_calendar_by_time_period():
    dc = DateConverter()
    start_time, end_time = dc.convert_dateperiod('diese Woche')

    gct = GoogleCalendarTasks()
    appointment = gct.search_google_calendar_by_time(start_time, end_time)


def test_search_google_calendar_by_time_today():
    dc = DateConverter()
    start_time, end_time = dc.convert_relativedate('heute')

    gct = GoogleCalendarTasks()
    appointment = gct.search_google_calendar_by_time(start_time, end_time)


def test_search_google_calendar_by_time_weekend():
    dc = DateConverter()
    start_time, end_time = dc.convert_dateperiod('wochenende')

    gct = GoogleCalendarTasks()
    appointment = gct.search_google_calendar_by_time(start_time, end_time)

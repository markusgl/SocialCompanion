from google_calendar_tasks import GoogleCalendarTasks
from date_converter import DateConverter


def test_search_google_calendar_by_time():
    dc = DateConverter()
    start_time, end_time = dc.convert_dateperiod('diese Woche')

    gct = GoogleCalendarTasks()
    gct.search_google_calendar_by_time(start_time, end_time)

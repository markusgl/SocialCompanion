import os
import datetime
import logging

from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from fuzzywuzzy import fuzz

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class GoogleCalendarTasks:

    @staticmethod
    def search_google_calendar_by_time(start_time, end_time):
        """
        :param start_time: datetime object
        :param end_time: days to be parsed as integer
        :return: list of events
        """
        # calculate max time for one day
        time_max = start_time + timedelta(days=end_time)
        time_max = time_max.replace(hour=23, minute=59, second=59, microsecond=0)
        time_max = time_max.isoformat() + 'Z'

        start_time = start_time.replace(hour=0, minute=0, second=1, microsecond=0)
        start_time = start_time.isoformat() + 'Z'

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage(ROOT_DIR + '/credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(ROOT_DIR + '/client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()), cache_discovery=False)

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=start_time, timeMax=time_max,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    def search_google_calendar_by_subject(self, subject):
        # search the next ten appointments for the corresponding subject
        today = datetime.datetime.now()
        event_time = today.isoformat() + 'Z'

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage(ROOT_DIR + '/credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(ROOT_DIR + '/client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()), cache_discovery=False)

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=event_time,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])

        appointment = None
        if not events:
            logging.debug('No upcoming events found.')
            return None
        for event in events:
            event_subject = event['summary']

            # fuzzy search of the projected subject
            fuzzy_ratio = fuzz.ratio(event_subject, subject)
            if fuzzy_ratio > 85:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['start'].get('dateTime', event['start'].get('date'))
                converted_start_date = datetime.datetime.strptime(start[:(len(start) - 6)], '%Y-%m-%dT%H:%M:%S')
                converted_end_date = datetime.datetime.strptime(start[:(len(end) - 6)], '%Y-%m-%dT%H:%M:%S')
                appointment = str(converted_start_date) + " - " + str(converted_end_date) + ": " + event_subject

        return appointment

    def create_event_in_google_calendar(self, start_datetime, end_datetime, subject, location=""):
        """
        :param start_datetime: datetime object
        :param end_datetime: days to be parsed as integer
        :param subject: string for the subject
        :param location: string for the location
        :return:
        """

        # logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
        # transform datetimes to iso format
        start_datetime = start_datetime.isoformat()
        end_datetime = end_datetime.isoformat()

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage(ROOT_DIR + '/credentials_create_event.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(ROOT_DIR + '/client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()), cache_discovery=False)

        if subject:
            # create event object
            event = {
                'summary': subject,
                'location': location,
                'description': '',
                'start': {
                    'dateTime': start_datetime,
                    'timeZone': 'Europe/Berlin',
                },
                'end': {
                    'dateTime': end_datetime,
                    'timeZone': 'Europe/Berlin',
                }
            }

            # Call the Calendar API
            event = service.events().insert(calendarId='primary', body=event).execute()
            logging.info('Calendar event created: %s' % (event.get('htmlLink')))
        else:
            return None

        return []


if __name__ == '__main__':
    from date_converter import DateConverter
    dc = DateConverter()
    start_time, end_time = dc.convert_dateperiod('diese Woche')

    gct = GoogleCalendarTasks()
    appointment = gct.search_google_calendar_by_time(start_time, end_time)
    print(type(appointment))

""" Custom Actions for API calls etc """
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet, AllSlotsReset, Restarted, UserUttered
from datetime import timedelta
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from fuzzywuzzy import fuzz
import logging
import re


class ActionSearchAppointment(Action):
    """
    Searches an appointments in the google calendar
    - if date and or time is given in any form, it will search for an event at that time
    - if only a subject is given, it will search for an appropriate event in the next days
    """

    def name(self):
        return 'action_search_appointment'

    def run(self, dispatcher, tracker, domain):
        # check if time was given by the user and convert relative dates and time periods
        appointment_start_time = ""
        appointment_end_time = 0

        if tracker.get_slot('date'):
            appointment_start_time = tracker.get_slot('date')
        elif tracker.get_slot('relativedate'):
            given_time = tracker.get_slot('relativedate')

            if given_time == 'heute':
                appointment_start_time = datetime.datetime.now()
            elif given_time == 'morgen':
                appointment_start_time = datetime.datetime.now() + timedelta(days=1)
            elif given_time == 'übermorgen':
                appointment_start_time = datetime.datetime.now() + timedelta(days=2)
            else:
                appointment_start_time = ""
        elif tracker.get_slot('dateperiod'):
            given_time = tracker.get_slot('dateperiod')
            if fuzz.ratio(given_time, 'nächste tage') > 85:
                appointment_start_time = datetime.datetime.now()
                appointment_end_time = 4
            elif fuzz.ratio(given_time, 'wochenende') > 85:
                # calculate days until weekend depending on weekday
                weekno = datetime.datetime.now().weekday()
                if weekno < 4:
                    delta = 4 - weekno
                    appointment_start_time = datetime.datetime.now() + timedelta(days=delta)
                else:
                    appointment_start_time = datetime.datetime.now()

                appointment_end_time = appointment_start_time + timedelta(days=2)

        if appointment_start_time:
            events = self.search_google_calendar_by_time(appointment_start_time, appointment_end_time)
            if not events:
                dispatcher.utter_message("Du hast heute keine Termine.")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                conv_date = datetime.datetime.strptime(start[:(len(start) - 6)], '%Y-%m-%dT%H:%M:%S')

                dispatcher.utter_message("Ich konnte folgende Termine für " + conv_date.strftime('%d.%m.%Y') + " finden: ")
                dispatcher.utter_message(conv_date.strftime('%H:%M') + " " + event['summary'])

        # if only activity (subject) is given search by subject
        elif tracker.get_slot('activity'):
            subject = tracker.get_slot('activity')
            dispatcher.utter_message("Ich sehe mal nach ob ich einen Termin zum Thema " + subject.title() + "finden kann.")
            event = self.search_google_calendar_by_subject(subject)
            if event:
                dispatcher.utter_message("Ich konnte folgende Termine finden " + event)
            else:
                dispatcher.utter_message(
                    "Ich konnte leider keinen Termin zum Thema " + subject.title() + " finden.")

        return []

    def search_google_calendar_by_time(self, start_time, end_time):
        """
        :param start_time: datetime object
        :param end_time: days to be parsed
        :return:
        """
        # calculate max time for one day
        time_max = start_time + timedelta(days=end_time)
        time_max = time_max.replace(hour=23, minute=59, second=59, microsecond=0)
        time_max = time_max.isoformat() + 'Z'

        #logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
        start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        start_time = start_time.isoformat() + 'Z'

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()), cache_discovery=False)

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=start_time, timeMax=time_max,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        for event in events:
            print(event['summary'])

        return events

    def search_google_calendar_by_subject(self, subject):
        #logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
        # search the next ten appointments for the corresponding subject
        today = datetime.datetime.now()
        event_time = today.isoformat() + 'Z'

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()), cache_discovery=False)

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=event_time,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])

        appointment = None
        if not events:
            print('No upcoming events found.')
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
                print(str(converted_start_date) + " - " + str(converted_end_date) + ": " + event_subject)
                appointment = str(converted_start_date) + " - " + str(converted_end_date) + ": " + event_subject

        return appointment


class ActionMakeAppointment(Action):
    def name(self):
        return 'action_make_appointment'

    def run(self, dispatcher, tracker, domain):
        #if tracker.get_slot('end_time'):
        #   end_time = tracker.get_slot('end_time')
        # use default duration of 1 hour if end_time is not given
        #else:
        #    end_time = start_time
        date = ""
        if tracker.get_slot('relativedate'):
            rel_date = tracker.get_slot('relativedate')
            if rel_date == "heute":
                time_delta = 0
            elif rel_date == "morgen":
                time_delta = 1
            elif rel_date == "übermorgen":
                time_delta = 2
            else:
                time_delta = 0
            date = datetime.datetime.now() + timedelta(days=time_delta)
            date = date.strftime('%Y-%m-%d')

        elif tracker.get_slot('date'):
            # extract date from string
            match = re.search(r'[0-9]{1,2}\.[0-9]{1,2}(\.)?([0-9]{4}|[0-9]{2})?', tracker.get_slot('date'))
            if match:
                date = match.group()
            else:
                return


        #elif tracker.get_slot('dateperiod'):
            #TODO


        else:
            return

        if tracker.get_slot('start_time') and tracker.get_slot('subject'):
            # convert the given time to datetime format
            start_time = tracker.get_slot('start_time')

            # TODO
            # extract time from string
            match = re.search(r'[0-9]{1,2}(:|\.)?([0-9]{1,2})?', start_time)
            if match:
                start_time = match.group()
            subject = tracker.get_slot('subject')

            self.create_event_in_google_calendar(start_time)
        else:
            dispatcher.utter_message("Mir fehlen leider noch Information zur Erstellung des Termins.")

        return []

    def create_event_in_google_calendar(self, start_time, end_time, subject, location=""):
        """
        :param start_time: datetime object
        :param end_time: days to be parsed as integer
        :param subject: string for the subject
        :param location: string for the location
        :return:
        """

        # logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
        # transform datetimes to iso format
        start_time = start_time.isoformat()
        end_time = end_time.isoformat()

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage('credentials_create_event.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()), cache_discovery=False)

        if subject:
            # create event object
            event = {
                'summary': subject,
                'location': location,
                'description': '',
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'Europe/Berlin',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Europe/Berlin',
                },
                'recurrence': [
                    'RRULE:FREQ=DAILY;COUNT=2'
                ]
            }

            # Call the Calendar API
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
        else:
            return None

        return []


class ActionPhoneCall(Action):
    def name(self):
        return 'action_phone_call'

    def run(self, dispatcher, tracker, domain):
        # TODO

        return []

class ActionReadNews(Action):
    def name(self):
        return 'action_read_news'

    def run(self, dispatcher, tracker, domain):
        # TODO

        return []


class ActionClearSlots(Action):
    def name(self):
        return 'action_clear_slots'

    def run(self, dispatcher, tracker, domain):
        tracker.clear_follow_up_action()

        print("Current slot-values %s" % tracker.current_slot_values())
        print("Current state %s" % tracker.current_state())

        return [AllSlotsReset()]


class ActionRestarted(Action):
    def name(self):
        return 'action_restarted'

    def run(self, dispatcher, tracker, domain):
        return[Restarted()]


# for testing
if __name__ == '__main__':
    # test search_calendar by time
    """
    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    ActionSearchAppointment().search_google_calendar_by_time(today, 2)
    """
    # test search calendar by subject
    ActionSearchAppointment().search_google_calendar_by_subject('Arzt')

    """
    # test create calendar event
    start_time = datetime.datetime.strptime('30 08 2018 13 00', '%d %m %Y %H %M')
    end_time = datetime.datetime.strptime('30 08 2018 14 00', '%d %m %Y %H %M')

    ActionMakeAppointment().create_event_in_google_calendar(start_time, end_time, 'Test')
    """
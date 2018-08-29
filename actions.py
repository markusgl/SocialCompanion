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


class ActionSearchAppointment(Action):
    """
    Searches appointments on the google calendar depending on given time or time period
    """
    def name(self):
        return 'action_search_appointment'

    def run(self, dispatcher, tracker, domain):
        # check if time was given by the user and convert relative dates and time periods
        if tracker.get_slot('date'):
            appointment_start_time = tracker.get_slot('date')
        elif tracker.get_slot('relativedate'):
            given_time = tracker.get_slot('relativedate')
            appointment_end_time = 0
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

        elif tracker.get_slot('activity'):
            subject = tracker.get_slot('activity')
            event = self.search_google_calendar_by_subject(subject)
            if event:
                dispatcher.utter_message("Ich konnte folgende Termine finden " + event)
            else:
                dispatcher.utter_message("Ich konnte leider keinen Termin zum Thema " + subject.title() + " finden.")

        else:
            appointment_start_time = ""

        if appointment_start_time:
            events = self.search_google_calendar_by_time(appointment_start_time, appointment_end_time)
            if not events:
                dispatcher.utter_message("Du hast heute keine Termine.")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                conv_date = datetime.datetime.strptime(start[:(len(start) - 6)], '%Y-%m-%dT%H:%M:%S')

                dispatcher.utter_message("Ich konnte folgende Termine für " + conv_date.strftime('%d.%m.%Y') + " finden: ")
                dispatcher.utter_message(conv_date.strftime('%H:%M') + " " + event['summary'])

                #print(start, event['summary'])
        elif tracker.get_slot('activity'):
            subject = tracker.get_slot('activity')
            event = self.search_google_calendar_by_subject(subject)
            if event:
                dispatcher.utter_message(event)

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
        # search the next tow weeks for the corresponding subject
        after_tomorrow = datetime.datetime.now()
        event_time = after_tomorrow.isoformat() + 'Z'

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
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['start'].get('dateTime', event['start'].get('date'))

            # fuzzy search of the projected subject
            fuzzy_ratio = fuzz.ratio(event_subject, subject)
            if fuzzy_ratio > 85:
                converted_start_date = datetime.datetime.strptime(start[:(len(start) - 6)], '%Y-%m-%dT%H:%M:%S')
                converted_end_date = datetime.datetime.strptime(start[:(len(end) - 6)], '%Y-%m-%dT%H:%M:%S')
                print(str(converted_start_date) + " - " + str(converted_end_date) + ": " + event_subject)
                appointment = str(converted_start_date) + " - " + str(converted_end_date) + ": " + event_subject

        return appointment

if __name__ == '__main__':
    # for testing
    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    ActionSearchAppointment().search_google_calendar_by_time(today, 2)



class ActionMakeAppointment(Action):
    def name(self):
        return 'action_make_appointment'

    def run(self, dispatcher, tracker, domain):
        # TODO

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


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
from google_news_searcher import GoogleNewsSearcher

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

        if tracker.get_slot('time') and tracker.get_slot('activity'):
            if tracker.get_slot('relativedate'):
                start_date = self.convert_date(tracker.get_slot('relativedate'), 'relativedate')
            elif tracker.get_slot('date'):
                start_date = self.convert_date(tracker.get_slot('date'), 'date')
            #elif tracker.get_slot('dateperiod'):
                #TODO
            else:
                return

            hour, minute = self.convert_time(tracker.get_slot('time'))
            start_date = start_date.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)

            # use default duration of 1 hour if end_time is not given
            end_date = start_date
            end_date = end_date.replace(hour=int(hour)+1, minute=int(minute), second=0, microsecond=0)
            subject = tracker.get_slot('activity')

            self.create_event_in_google_calendar(start_date, end_date, subject)
            dispatcher.utter_message("Ok ich habe den Termin " + subject + " in den Kalendar eingetragen und werde dich erinnern.")
        else:
            dispatcher.utter_message("Mir fehlen leider noch Information zur Erstellung des Termins.")

        return []

    def convert_date(self, date_string, date_type):
        """
        gets at date as string and returns as datetime
        :param date_string: date as string in any format (e. g. heute, morgen, 1.1. etc.)
        :param date_type: type of the given date
        :return: date as datetime object
        """

        converted_date = ""
        if date_type == 'relativedate':
            rel_date = date_string
            if rel_date == "heute":
                time_delta = 0
            elif rel_date == "morgen":
                time_delta = 1
            elif rel_date == "übermorgen":
                time_delta = 2
            else:
                time_delta = 0
            converted_date = datetime.datetime.now() + timedelta(days=time_delta)
            converted_date = converted_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # if date is given as numbers
        if date_type == 'date':
            # extract dateformat from string
            match = re.search(r'[0-9]{1,2}\.[0-9]{1,2}(\.)?([0-9]{4}|[0-9]{2})?', date_string)
            if match:
                # print(match.group())
                date_array = str(match.group()).split('.')
            else:
                print('No match')
                date_array = ""

            # convert different possible date format to one equal
            if len(date_array) == 2:
                day = date_array[0].zfill(2)
                month = date_array[1].zfill(2)
                year = datetime.datetime.now().year

            elif len(date_array) == 3 and date_array[2] == "":
                day = date_array[0].zfill(2)
                month = date_array[1].zfill(2)
                year = datetime.datetime.now().year

            elif len(date_array) == 3:
                day = date_array[0].zfill(2)
                month = date_array[1].zfill(2)
                if len(date_array[2]) == 4:
                    year = date_array[2]
                elif len(date_array[2]) == 2:
                    year = '20' + date_array[2]

            converted_date = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d')
            print(type(converted_date))

        return converted_date


    def convert_time(self, time_string):
        """
        extract the time of a string and returns the hours and minutes
        :param time_string:
        :return: hour and minute
        """
        hour = 0
        minute = 0
        # extract time from string
        match = re.search(r'[0-9]{1,2}(:|\.)?([0-9]{1,2})?', time_string)
        if match:
            time_string = match.group()
            time_array = re.split('(\.|:)', time_string)
        else:
            return

        if len(time_array) == 1:
            hour = time_array[0].zfill(2)
            minute = '00'
        elif len(time_array) == 3:
            hour = time_array[0].zfill(2)
            minute = time_array[2].zfill(2)

        return hour, minute


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
            print('Event created: %s' % (event.get('htmlLink')))
        else:
            return None

        return []


class ActionReadNews(Action):
    def name(self):
        return 'action_read_news'

    def run(self, dispatcher, tracker, domain):

        if tracker.get_slot('news_type'):
            topic = tracker.get_slot('news_type')
            news_list = GoogleNewsSearcher().search_news(topic)
            dispatcher.utter_message("Hier sind die 10 Schlagzeilen zum Thema " + topic + ":")

        else:
            news_list = GoogleNewsSearcher().search_news()
            dispatcher.utter_message("Hier sind die 10 aktuellen Schlagzeilen:")

        news_utterance = ""
        for i in range(len(news_list)):
            if i != 0:
                #dispatcher.utter_message(news_list[i].title.text)
                news_utterance += "\n" + news_list[i].title.text

        dispatcher.utter_message(news_utterance)

        return []


class ActionPhoneCall(Action):
    def name(self):
        return 'action_phone_call'

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
    """
    # test search calendar by subject
    ActionSearchAppointment().search_google_calendar_by_subject('Arzt')

    
    # test create calendar event
    start_time = datetime.datetime.strptime('31 08 2018 13 00', '%d %m %Y %H %M')
    end_time = datetime.datetime.strptime('31 08 2018 14 00', '%d %m %Y %H %M')

    ActionMakeAppointment().create_event_in_google_calendar(start_time, end_time, 'Test')
    """

    print(ActionMakeAppointment().convert_date('1.1.', 'date'))

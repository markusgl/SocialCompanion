import datetime

from rasa_core.actions.action import Action

from google_calendar_tasks import GoogleCalendarTasks
from date_converter import DateConverter
from speech_handling.text_to_speech import TextToSpeech


class ActionSearchAppointment(Action):
    """
    Searches an appointments in the google calendar
    - if date and or time is given in any form, it will search for an event at that time
    - if only a subject is given, it will search for an appropriate event in the next days
    """

    def name(self):
        return 'action_search_appointment'

    def run(self, dispatcher, tracker, domain):
        # utter wait message
        dispatcher.utter_message("Einen Augenblick. Ich sehe mal im Kalender nach.")
        TextToSpeech().utter_voice_message("Einen Augenblick. Ich sehe mal im Kalender nach.")
        date_conv = DateConverter()

        # check if time was given by the user and convert relative dates and time periods
        if tracker.get_slot('date'):
            given_date = tracker.get_slot('date')
            start_time = given_date
            end_time = 0
            bot_reply_message = self._generate_reply_message_with_date(start_time, end_time)
        elif tracker.get_slot('relativedate'):
            given_date = tracker.get_slot('relativedate')
            start_time, end_time = date_conv.convert_relativedate(given_date)
            bot_reply_message = self._generate_reply_message_with_date(start_time, end_time)
        elif tracker.get_slot('dateperiod'):
            given_date = tracker.get_slot('dateperiod')
            start_time, end_time = date_conv.convert_dateperiod(given_date)
            bot_reply_message = self._generate_reply_message_with_date(start_time, end_time)
        elif tracker.get_slot('activity'): # if only activity (subject) is given search an event by activity name
            subject = tracker.get_slot('activity')

            bot_reply_message = self._generate_reply_message_with_subject(subject)
        else:
            bot_reply_message = "Mir fehlen leider noch Informationen, wie Betreff oder Uhrzeit, zum Finden deiner Termine."

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)

        return []

    @staticmethod
    def _generate_reply_message_with_subject(subject):
        gcal_tasks = GoogleCalendarTasks()
        bot_reply_message = "Ich sehe mal nach ob ich einen Termin zum Thema " + subject.title() + "finden kann. \n"

        event = gcal_tasks.search_google_calendar_by_subject(subject)
        if event:
            bot_reply_message += "Ich konnte folgende Termine finden " + event
        else:
            bot_reply_message += "Ich konnte leider keinen Termin zum Thema " + subject.title() + " finden."

        return bot_reply_message

    @staticmethod
    def _generate_reply_message_with_date(start_time, end_time):
        gcal_tasks = GoogleCalendarTasks()
        events = gcal_tasks.search_google_calendar_by_time(start_time, end_time)
        date_format = start_time.strftime('%d.%m.%Y')

        if events:
            bot_reply_message = "Ich konnte folgende Termine für {} finden:\n".format(date_format)
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))

                if len(start) == 10:  # full-day events without time indication
                    conv_date = datetime.datetime.strptime(start, '%Y-%m-%d')
                    bot_reply_message += "(Ganztägig) {}\n".format(conv_date.strftime('%d.%m.%Y'), event['summary'])
                else:  # non full-day events including specific time
                    conv_date = datetime.datetime.strptime(start[:(len(start) - 6)], '%Y-%m-%dT%H:%M:%S')
                    bot_reply_message += "{} {}\n".format(conv_date.strftime('%H:%M'),
                                                          event['summary'])
        else:
            bot_reply_message = "Du hast heute keine Termine."

        return bot_reply_message


class ActionMakeAppointment(Action):
    def name(self):
        return 'action_make_appointment'

    def run(self, dispatcher, tracker, domain):
        date_conv = DateConverter()
        gcal_tasks = GoogleCalendarTasks()

        if tracker.get_slot('time') and tracker.get_slot('activity'):
            if tracker.get_slot('relativedate'):
                start_date = date_conv.convert_date(tracker.get_slot('relativedate'), 'relativedate')
            elif tracker.get_slot('date'):
                start_date = date_conv.convert_date(tracker.get_slot('date'), 'date')
            #elif tracker.get_slot('dateperiod'):
                #TODO
            else:
                return

            hour, minute = date_conv.convert_time(tracker.get_slot('time'))
            start_date = start_date.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)

            # use default duration of 1 hour if end_time is not given
            end_date = start_date
            end_date = end_date.replace(hour=int(hour)+1, minute=int(minute), second=0, microsecond=0)
            subject = tracker.get_slot('activity')

            gcal_tasks.create_event_in_google_calendar(start_date, end_date, subject)
            bot_reply_message = "Ok ich habe den Termin " + subject + " in den Kalendar eingetragen und werde dich erinnern."
        else:
            bot_reply_message = "Mir fehlen leider noch Information zur Erstellung des Termins."

        dispatcher.utter_message(bot_reply_message)
        TextToSpeech().utter_voice_message(bot_reply_message)

        return []

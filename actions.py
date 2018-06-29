""" Custom Actions for API calls etc """
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.forms import EntityFormField

from knowledge_base.knowledge_graph import KnowledgeGraph

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet, AllSlotsReset, Restarted, UserUttered
from datetime import timedelta
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import logging


class ActionSearchContact(Action):
    def name(self):
        return 'action_search_contact'

    def run(self, dispatcher, tracker, domain):
        kg = KnowledgeGraph()
        contact_name = tracker.get_slot('firstname')
        relation_ship = tracker.get_slot('relationship')
        me_name = tracker.get_slot('me_name')

        # search relationship by contact name
        if me_name and contact_name:
            relationship = kg.search_relationship_by_contactname(me_name, contact_name)
            if relationship is None:
                dispatcher.utter_message("Ich kenne " + str(contact_name).title() + " nicht. Willst du mir sagen wer das ist?")
            else:
                SlotSet("relationship", relationship)
                dispatcher.utter_message("Deine(n) " + relationship + " " + str(contact_name).title() +"?")

        # search contact name by given relationship
        elif me_name and relation_ship:
            contact = kg.search_contactname_by_relationship(me_name, relation_ship)
            if contact is None:
                if relation_ship == "vater" or relation_ship == "bruder" or relation_ship == "onkel":
                    dispatcher.utter_message("Ich kenne deinen " + str(relation_ship).title() + " leider nicht. "
                                                                                   "Willst du mir sagen wie er heißt?")
                elif relation_ship == "mutter" or relation_ship == "schwester" or relation_ship == "tante":
                    dispatcher.utter_message("Ich kenne deine " + str(relation_ship).title() + " leider."
                                                                                  "Willst du mir sagen wie sie heißt?")
                else:
                    dispatcher.utter_message("Ich kenne " + str(relation_ship) + " nicht.")
            else:
                SlotSet("contactname", contact)
                dispatcher.utter_message("Meinst du "+contact+"?")
        elif not me_name:
            dispatcher.utter_message("Leider kenne ich dich noch nicht und auch deine Kontkate nicht. "
                                     "Willst du mir sagen wie du heißt?")
        else:
            dispatcher.utter_message("Leider hab ich dich nicht ganz verstanden. Wen willst du mitnehmen?")

        return []


class ActionAddContact(Action):
    def name(self):
        return 'action_add_contact'

    def run(self, dispatcher, tracker, domain):
        kg = KnowledgeGraph()

        me_name = tracker.get_slot('me_name')
        contactname = tracker.get_slot('firstname')
        relationship = tracker.get_slot('relationship')

        if me_name and contactname and relationship:
            print("try to add contact")
            kg.add_contact(me_name, contactname, relationship)
            dispatcher.utter_message("Danke, jetzt kenne ich auch " + str(contactname).title() + "!")
        else:
            dispatcher.utter_message("Ich habe deinen Kontakt und die Beziehung leider nicht verstanden. Willst du mir sie nochmal sagen?")


class ActionSearchMe(Action):
    def name(self):
        return 'action_search_me'

    def run(self, dispatcher, tracker, domain):
        kg = KnowledgeGraph()
        me_name = tracker.get_slot('firstname')
        if me_name:
            exist = kg.get_me_by_name(me_name)
            if exist:
                dispatcher.utter_message("Der Name " + me_name.title() + " kommt mir bekannt vor! Kennen wir uns bereits?")
            else:
                #ActionAddMe.run(dispatcher, tracker, domain)
                kg.add_me(me_name)
                dispatcher.utter_message("Hallo " + me_name.title() + "! Schön von dir zu hören.")

        return [SlotSet('me_name', me_name), SlotSet('firstname', None)]


class ActionAddMe(Action):
    """
    Add the central user i.e. 'Me' if it does not exits yet
    """
    def name(self):
        return 'action_add_me'

    def run(self, dispatcher, tracker, domain):
        kg = KnowledgeGraph()
        me_name = tracker.get_slot('me_name')

        if me_name:
            kg.add_me(me_name)
            dispatcher.utter_message("Hallo " + str(me_name).title() + "! Schön von dir zu hören.")

        return [SlotSet('me_name', me_name), SlotSet('firstname', None)]


class ActionSearchEvents(Action):
    """
    Searches eveent recommendations in the area and suggests contacts to join
    """
    #@staticmethod
    #def required_fields(self):
    #    return[
    #        EntityFormField("location", "location"),
    #        EntityFormField("dateperiod", "datetime", "relativedate")
    #    ]

    def name(self):
        return 'action_search_events'

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot('location')

        if tracker.get_slot('datetime'):
            time = tracker.get_slot('datetime')
        elif tracker.get_slot('relativedate'):
            time = tracker.get_slot('relativedate')
            if time == 'morgen':
                tomorrow = datetime.datetime.now() + timedelta(days=1)
                event_time = tomorrow.isoformat() + 'Z'

        elif tracker.get_slot('dateperiod'):
            time = tracker.get_slot('dateperiod')

            #TODO convert to date
        else:
            event_time = None

        dispatcher.utter_message("Ich versuche Veranstaltungen in deiner Umgebung zu finden")

        #activity = tracker.get_slot('activity')
        print("Current slot-values %s" % tracker.current_slot_values())
        print("Current state %s" % tracker.current_state())

        return []


class ActionSearchAppointment(Action):
    """
    Searches appointments on the google calendar depending on given time or time period
    """
    def name(self):
        return 'action_search_appointment'

    def run(self, dispatcher, tracker, domain):
        # check if time was given by the user and convert relative dates and time periods
        if tracker.get_slot('datetime'):
            appointment_time = tracker.get_slot('datetime')
        elif tracker.get_slot('relativedate'):
            given_time = tracker.get_slot('relativedate')
            if given_time == 'heute':
                today = datetime.datetime.now()
                appointment_time = today.isoformat() + 'Z'
            elif given_time == 'morgen':
                tomorrow = datetime.datetime.now() + timedelta(days=1)
                appointment_time = tomorrow.isoformat() + 'Z'
            elif given_time == 'übermorgen':
                after_tomorrow = datetime.datetime.now() + timedelta(days=2)
                appointment_time = after_tomorrow.isoformat() + 'Z'
            else:
                appointment_time = ""
        elif tracker.get_slot('dateperiod'):
            given_time = tracker.get_slot('dateperiod')
            appointment_time = ""
        else:
            appointment_time = ""

        if appointment_time:
            print(appointment_time)
            events = self.search_google_calendar(appointment_time)
            if not events:
                dispatcher.utter_message("Du hast heute keine Termine.")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                conv_date = datetime.datetime.strptime(start[:(len(start) - 6)], '%Y-%m-%dT%H:%M:%S')

                dispatcher.utter_message("Ich konnte folgende Termine für " + conv_date.strftime('%d.%m.%Y') + " finden: ")
                dispatcher.utter_message(conv_date.strftime('%H:%M') + " " + event['summary'])

                #print(start, event['summary'])

        return []

    def search_google_calendar(self, event_time):
        #logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)
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
        print(events_result)
        events = events_result.get('items', [])
        print(events)

        final_events = []
        if not events:
            print('No upcoming events found.')
            return None
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            conv_date = datetime.datetime.strptime(start[:(len(start) - 6)], '%Y-%m-%dT%H:%M:%S')
            today = datetime.datetime.today().strftime('%Y-%m-%d')

            #print(start, event['summary'])ö

        return events

if __name__ == '__main__':
    today = datetime.datetime.now()
    appointment_time = today.isoformat() + 'Z'
    ActionSearchAppointment().search_google_calendar(appointment_time)


class ActionSuggest(Action):
    def name(self):
        return 'action_suggest'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Ich konnte folgendes finden")
        count = 1
        for match in tracker.get_slot("matches"):
            dispatcher.utter_message(str(count) + " " + match)
            count += 1
        dispatcher.utter_message("Wie ist deine Wahl?")
        dispatcher.utter_button_message("Tippe die entsprechende Zahl ein", buttons=[{"1":"eins", "2":"zwei", "3":"drei"}])

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


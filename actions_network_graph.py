"""
Actions for task related to the network graph, e.g. adding/deleting user to/from the network
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from network_core.network_graph import NetworkGraph

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

from analytics_engine.analytics import AnalyticsEngine
from analytics_engine.relation_extractor import LANG

import logging

gender_dict = {"frau": "female", "fr.": "female", "herr": "male", "hr.": "male"}


class ActionSearchMe(Action):
    def name(self):
        return 'action_search_me'

    def run(self, dispatcher, tracker, domain):
        kg = NetworkGraph()
        bot_reply_message = "Ich habe deinen Namen nicht verstanden. Kannst du ihn noch einmal sagen?"
        me_name = ""

        if tracker.get_slot('firstname'):
            me_name = tracker.get_slot('firstname')
            me_node = kg.get_me_by_firstname(me_name)
            if not me_node:
                kg.add_me_w_firstname(me_name)
                bot_reply_message = "Hallo " + me_name.title() + "! Schön dich kennen zu lernen. \n Wie alt bist du?"
            else:
                bot_reply_message = "Hallo " + me_name.title() + "! Wir kennen uns bereits nicht wahr?"

        elif tracker.get_slot('lastname'):
            me_name = tracker.get_slot('lastname')
            me_node = kg.get_me_by_lastname(me_name)
            if me_node:  # known user
                if me_node.gender == 'female':
                    salutation = 'Frau ' + me_name.title()
                elif me_node.gender == 'male':
                    salutation = 'Herr ' + me_name.title()
                else:
                    salutation = "Herr oder Frau" + me_name.title()
                bot_reply_message = "Hallo " + salutation + "! Wir kennen uns bereits nicht wahr?"
            else:  # unknown user
                if tracker.get_slot('gender') and tracker.get_slot('gender') in gender_dict.keys():
                    gender = gender_dict[tracker.get_slot('gender')]
                    if gender == 'female':
                        salutation = "Frau " + me_name.title()
                    else:
                        salutation = "Herr " + me_name.title()
                else:
                    salutation = "Herr oder Frau " + me_name.title()
                    gender = ""

                bot_reply_message = "Hallo " + salutation + "! Schön dich kennen zu lernen.\n Wie alt bist du?"

                kg.add_me_w_lastname(me_name, gender=gender, age="")

        # Response
        dispatcher.utter_message(bot_reply_message)

        return [SlotSet('me_name', me_name), SlotSet('firstname', None)]


class ActionAddMe(Action):
    """
    Add the central user i.e. 'Me' if it does not exits yet
    """
    def name(self):
        return 'action_add_me'

    def run(self, dispatcher, tracker, domain):
        kg = NetworkGraph()
        me_name = tracker.get_slot('me_name')
        bot_reply_message = ""

        if me_name:
            kg.add_me_w_firstname(me_name)
            bot_reply_message = "Hallo " + str(me_name).title() + "! Schön dich kennen zu lernen. Wie alt bist du?"

        dispatcher.utter_message(bot_reply_message)

        return [SlotSet('me_name', me_name), SlotSet('firstname', None)]


class ActionSearchContact(Action):
    def name(self):
        return 'action_search_contact'

    def run(self, dispatcher, tracker, domain):
        kg = NetworkGraph()
        contact_name = tracker.get_slot('firstname')
        relation_ship = tracker.get_slot('relationship')
        me_name = tracker.get_slot('me_name')
        utterance = tracker.latest_message()
        ae = AnalyticsEngine(lang=LANG.DE)

        # search relationship by contact name
        if me_name and contact_name:
            relationship = kg.search_relationship_by_contactname(me_name, contact_name)

            if relationship:
                SlotSet("relationship", relationship)
                dispatcher.utter_message("Deine(n) " + relationship + " " + str(contact_name).title() +"?")
            else:
                ae.analyze_utterance(utterance, persist=True)

        # search contact name by given relationship
        elif me_name and relation_ship:
            contact = kg.search_contactname_by_relationship(me_name, relation_ship)

            if contact:  # contact already exists in network
                SlotSet("contactname", contact)
                dispatcher.utter_message("Meinst du "+contact+"?")
            else:
                ae.analyze_utterance(utterance, persist=True)

        elif me_name:
            dispatcher.utter_message("Leider hab ich dich nicht ganz verstanden. Wen willst du mitnehmen?")
        else:
            dispatcher.utter_message("Leider kenne ich dich noch nicht und auch deine Kontkate nicht. "
                                     "Willst du mir sagen wie du heißt?")


class ActionAddContact(Action):
    def name(self):
        return 'action_add_contact'

    def run(self, dispatcher, tracker, domain):
        kg = NetworkGraph()

        me_name = tracker.get_slot('me_name')
        contactname = tracker.get_slot('firstname')
        relationship = tracker.get_slot('relationship')

        if me_name and contactname and relationship:
            kg.add_contact(me_name, contactname, relationship)
            dispatcher.utter_message("Schön, jetzt kenne ich auch " + str(contactname).title() + "!")
        else:
            dispatcher.utter_message("Ich habe den Namen leider nicht verstanden. Willst du mir sie nochmal sagen?")

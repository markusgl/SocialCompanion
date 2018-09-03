""" Custom Actions for API calls etc """
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from network_graph.network_graph import NetworkGraph

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet, AllSlotsReset, Restarted, UserUttered
from speech_handling.text_to_speech import TextToSpeech

import logging

gender_dict = {"frau": "female", "fr.": "female", "herr": "male", "hr.": "male"}


class ActionSearchMe(Action):
    def name(self):
        return 'action_search_me'

    def run(self, dispatcher, tracker, domain):
        kg = NetworkGraph()
        if tracker.get_slot('firstname'):
            me_name = tracker.get_slot('firstname')
            me_node = kg.get_me_by_firstname(me_name)
            if not me_node:
                kg.add_me_w_firstname(me_name)
                dispatcher.utter_message("Hallo " + me_name.title() + "! Schön von dir zu hören.")
            else:
                dispatcher.utter_message("Hallo " + me_name.title() + "! Wir kennen uns berits nicht wahr?.")
        elif tracker.get_slot('lastname'):
            me_name = tracker.get_slot('lastname')
            me_node = kg.get_me_by_lastname(me_name)
            if me_node:
                if me_node.gender == 'female':
                    dispatcher.utter_message("Hallo Frau " + me_name.title() + "! Wir kennen uns berits nicht wahr?.")
                    TextToSpeech().out_text_message("Hallo Frau " + me_name.title() + "! Wir kennen uns berits nicht wahr?.")
                elif me_node.gender == 'male':
                    dispatcher.utter_message("Guten Tag Herr " + me_name.title() + "! Wir kennen uns bereits nicht wahr?.")
                    TextToSpeech().out_text_message(
                        "Guten Tag Herr " + me_name.title() + "! Wir kennen uns bereits nicht wahr?.")
                else:
                    dispatcher.utter_message(
                        "Hallo Herr oder Frau " + me_name.title() + "! Freut mich Sie kennenzulernen.")
                    TextToSpeech().out_text_message(
                        "Guten Tag Herr oder Frau" + me_name.title() + "! Freut mich Sie kennenzulernen.")
            else:
                if tracker.get_slot('gender') and tracker.get_slot('gender') in gender_dict.keys():
                    gender = gender_dict[tracker.get_slot('gender')]
                    if gender == 'female':
                        dispatcher.utter_message("Guten Tag Frau " + me_name.title() + "! Schön von Ihnen zu hören.")
                    elif gender == 'male':
                        dispatcher.utter_message("Hallo Herr " + me_name.title() + "! Schön von Ihnen zu hören.")
                else:
                    dispatcher.utter_message("Hallo Herr oder Frau " + me_name.title() + "! Freut mich Sie kennenzulernen.")
                    TextToSpeech().out_text_message(
                        "Hallo Herr oder Frau " + me_name.title() + "! Freut mich Sie kennenzulernen.")
                    gender = ""

                kg.add_me_w_lastname(me_name, gender=gender, age="")
        else:
            return None

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

        if me_name:
            kg.add_me_w_firstname(me_name)
            dispatcher.utter_message("Hallo " + str(me_name).title() + "! Schön von dir zu hören.")

        return [SlotSet('me_name', me_name), SlotSet('firstname', None)]


### CURRENTLY NOT USED ###
class ActionSearchContact(Action):
    def name(self):
        return 'action_search_contact'

    def run(self, dispatcher, tracker, domain):
        kg = NetworkGraph()
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
        kg = NetworkGraph()

        me_name = tracker.get_slot('me_name')
        contactname = tracker.get_slot('firstname')
        relationship = tracker.get_slot('relationship')

        if me_name and contactname and relationship:
            print("try to add contact")
            kg.add_contact(me_name, contactname, relationship)
            dispatcher.utter_message("Danke, jetzt kenne ich auch " + str(contactname).title() + "!")
        else:
            dispatcher.utter_message("Ich habe deinen Kontakt und die Beziehung leider nicht verstanden. Willst du mir sie nochmal sagen?")
""" Custom core Actions for:
    * Managing appointments on the personal calendar
    * Searching news article
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging

from rasa_core.actions.action import Action
from rasa_core.events import AllSlotsReset, Restarted


class ActionClearSlots(Action):
    def name(self):
        return 'action_clear_slots'

    def run(self, dispatcher, tracker, domain):
        tracker.clear_follow_up_action()

        logging.info("All Slots reset.")
        logging.debug("Current slot-values %s" % tracker.current_slot_values())
        logging.debug("Current state %s" % tracker.current_state())

        return [AllSlotsReset()]


class ActionRestarted(Action):
    def name(self):
        return 'action_restarted'

    def run(self, dispatcher, tracker, domain):
        return[Restarted()]

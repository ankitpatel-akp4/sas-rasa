# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
import logging


class ActionGreet(Action):

    def name(self) -> str:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        current_hour = datetime.now().hour
        logging.info(f"tracker: {str(tracker.sender_id)}")
        logging.info(f"domain: {str(domain)}")
        if 5 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        dispatcher.utter_message(text=f"{greeting}! Welcome to aiqahealth Bot. How can I assist you today? Whether you need help with booking an appointment, finding a doctor, or have a health-related question, I'm here to help.")

        return []

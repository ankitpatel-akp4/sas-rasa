from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
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
    
class ActionCheckAvailability(Action):

    def name(self) -> Text:
        return "action_doctor_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        doctor = tracker.get_slot("doctor")
        time = tracker.get_slot("time")

        # Replace this with your actual logic to check the doctor's availability
        availability = {
            "Dr. Smith": ["Friday", "10:00 AM"],
            "Dr. Johnson": ["next Monday morning", "10:00 AM"],
            "Dr. Green": ["tomorrow afternoon"],
            # Add the rest of the doctors and their available times
        }

        if doctor in availability and time in availability[doctor]:
            dispatcher.utter_message(text=f"{doctor} is available at {time}.")
            return [SlotSet("time", time), SlotSet("doctor", doctor)]
        else:
            dispatcher.utter_message(template="utter_ask_alternative_time")
            return [SlotSet("time", None)]


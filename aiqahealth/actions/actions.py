from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionCheckAvailability(Action):

    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.get_slot("time")
        # Simulate checking availability
        dispatcher.utter_message(text=f"Dr. John Smith is available at {time} tomorrow. Would you like to confirm this appointment?")
        return []

class ActionConfirmAppointment(Action):

    def name(self) -> Text:
        return "action_confirm_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.get_slot("time")
        # Simulate confirming appointment
        dispatcher.utter_message(text=f"Your appointment with Dr. John Smith is confirmed for {time} tomorrow. Is there anything else I can help you with?")
        return []
    
class ActionFunTime(Action):

    def name(self) -> Text:
        return "action_fun_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text=f"Neet implementation to fetch a joke")
        return []

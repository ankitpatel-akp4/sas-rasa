from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted, ConversationPaused
from rasa_sdk.executor import CollectingDispatcher

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="I am passing you to a human...")
        
        return [UserUtteranceReverted()]
    
    
    
class ActionBookAppointment(Action):

    def name(self) -> str:
        return "action_book_appointment"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        dispatcher.utter_message(text="Your appointment has been booked.")
        return []

class ActionViewAppointment(Action):

    def name(self) -> str:
        return "action_view_appointment"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        dispatcher.utter_message(text="Here are the details of your appointment.")
        return []

class ActionRescheduleAppointment(Action):

    def name(self) -> str:
        return "action_reschedule_appointment"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        dispatcher.utter_message(text="Your appointment has been rescheduled.")
        return []

class ActionCancelAppointment(Action):

    def name(self) -> str:
        return "action_cancel_appointment"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        dispatcher.utter_message(text="Your appointment has been cancelled.")
        return []
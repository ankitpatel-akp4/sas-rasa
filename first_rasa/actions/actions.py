from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

class ValidateBookAppointmentForm(FormValidationAction):
    
    def name(self) -> Text:
        return "validate_book_appointment_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        if not tracker.get_slot("doctor"):
            dispatcher.utter_message(response="utter_show_doctors")
        return slots_mapped_in_domain

    def validate_doctor(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        doctors = ["Dr. Smith", "Dr. Brown", "Dr. Patel", "Dr. Lee"]
        doctor_num_map = {"1": "Dr. Smith", "2": "Dr. Brown", "3": "Dr. Patel", "4": "Dr. Lee"}
        
        if slot_value in doctor_num_map:
            return {"doctor": doctor_num_map[slot_value]}
        elif slot_value in doctors:
            return {"doctor": slot_value}
        else:
            dispatcher.utter_message(text="Please choose a valid doctor from the list.")
            return {"doctor": None}

class ActionSubmitAppointment(Action):

    def name(self) -> Text:
        return "action_submit_appointment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        doctor = tracker.get_slot("doctor")
        appointment_date = tracker.get_slot("appointment_date")
        
        dispatcher.utter_message(text=f"Your appointment with {doctor} has been booked for {appointment_date}.")
        return []

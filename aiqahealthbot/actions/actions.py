from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (SlotSet, 
                             FollowupAction,
                             Restarted, 
                             AllSlotsReset
                            )
from datetime import datetime
import logging
from abc import ABC, abstractmethod

log = logging.getLogger(__name__)

class BaseCustomAction(Action, ABC):
    
    @abstractmethod
    def name(self) -> Text:
        raise NotImplementedError("An action must implement a name")
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        log.info("action => {}".format(self.name()))
        response_events = self.action(dispatcher, tracker, domain)
        response_events.append(FollowupAction("action_listen"))
        current_active_form = tracker.get_slot("current_active_form")
        if current_active_form:
            if current_active_form == "action_book_appointment":
                response_events.append(SlotSet("confirm_question","continue_with_appointment"))
                dispatcher.utter_message(text="Would you like to continue with appointment booking?")

        return response_events

    def action(self, dispatcher: CollectingDispatcher,
                     tracker: Tracker,
                     domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        raise NotImplementedError("Custom logic needs to be implemented in subclass")

class ActionDefaultFallback(BaseCustomAction):
    
    def name(self) -> Text:
        return "action_default_fallback"

    def action(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="I did not understand. Please rephrase or call at +918756523281 for human support.")
        return []

class ActionGreet(Action):

    def name(self) -> str:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        current_hour = datetime.now().hour
        logging.info(f"tracker: {str(tracker.sender_id)}")
        if 5 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        dispatcher.utter_message(text=f"{greeting}! I am aiqa health bot. How are you?")
        # dispatcher.utter_message(text=f"{greeting}! I am aiqa bot. How can I assist you?")
        return [FollowupAction("action_listen")]    

class ActionMoodGreat(BaseCustomAction):

    def name(self) -> str:
        return "action_mood_great"

    def action(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        dispatcher.utter_message(text=f"Perfect! How can I assist you today?")
        return [FollowupAction("action_listen")]    
    
class ActionAskBootMood(BaseCustomAction):

    def name(self) -> str:
        return "action_ask_boot_mood"

    def action(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        dispatcher.utter_message(text=f"I am good.")
        dispatcher.utter_message(text=f"How can I assist you today?")
        return [FollowupAction("action_listen")]    

class ActionMoodUnhappy(BaseCustomAction):

    def name(self) -> str:
        return "action_mood_unhappy"

    def action(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:

        dispatcher.utter_message(text=f"Sorry to hear that!")
        dispatcher.utter_message(text=f"How can I assist you today?")
        return [FollowupAction("action_listen")]    

class ActionGoodbye(Action):

    def name(self) -> str:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        log.info(f"tracker: {str(tracker.sender_id)}")

        dispatcher.utter_message(text=f"Bye, Take care.")

        return [Restarted(), AllSlotsReset()] 

class ActionActionThank(Action):

    def name(self) -> str:
        return "action_thank"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        log.info(f"tracker: {str(tracker.sender_id)}")

        dispatcher.utter_message(text=f"You are welcome!")

        return [Restarted(), AllSlotsReset()] 

class ActionAffirm(Action):
    def name(self) -> str:
        return "action_affirm"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        confirm_question = tracker.get_slot("confirm_question")
        log.info("action_affirm -> confirm_question: {}".format(confirm_question))
        if confirm_question == "appointment_confirm":
            return [SlotSet("appointment_confirm", True), FollowupAction("action_book_appointment")]
            
        elif confirm_question == "continue_with_appointment":
            return [FollowupAction("action_book_appointment")]
            
        dispatcher.utter_message(text="I didn't understand. Please rephrase.")    
        return [FollowupAction("action_listen"), SlotSet("confirm_question", None)]

class ActionDeny(Action):

    def name(self) -> str:
        return "action_deny"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        confirm_question = tracker.get_slot("confirm_question")
        response_events: list = [SlotSet("confirm_question", None)]
        log.info("action_deny -> confirm_question: {}".format(confirm_question))
        if confirm_question == "appointment_confirm":
            return [SlotSet("appointment_confirm", False), FollowupAction("action_book_appointment")]
        elif confirm_question == "continue_with_appointment":
            dispatcher.utter_message(text="Ok. What else can I help you with?")
            return response_events + [SlotSet("current_active_form", None)] + [FollowupAction("action_listen")]
            
        dispatcher.utter_message(text="I didn't understand. Please rephrase.")    
        return response_events + [FollowupAction("action_listen")]
 
class ActionBookAppointment(Action):
    def name(self) -> str:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        log.info(f"action_book_appointment")
        # self.extract_appointment_time(tracker)
        required_slots = ["appointment_doctor_name", "appointment_symptom", "appointment_confirm"]
        res_msg: Any = {}
        return_list: list = [FollowupAction("action_listen")]
        for slot in required_slots:
            log.info("action_book_appointment -> slot: {} => {}".format(slot, tracker.get_slot(slot)))
            if tracker.get_slot(slot) is None:
                if slot == "appointment_doctor_name":
                    res_msg = "Which doctor would you like to book an appointment with?"
                
                # elif slot == "appointment_time":
                #     res_msg = "What time would you like to book the appointment?"
                
                # elif slot == "appointment_day":
                #     res_msg = "On which day would you like to book the appointment?"
                
                elif slot == "appointment_symptom":
                    res_msg = "Please describe your symptoms."
                    
                elif slot == "appointment_confirm":
                    res_msg = "Please confirm your appointment."
                    dispatcher.utter_message(text=res_msg)
                    res_msg =  "doctor: {}\day: {}\ntime: {}\nsymptoms: {}\n".format(
                                    tracker.get_slot("appointment_doctor_name"),
                                    tracker.get_slot("appointment_day"),
                                    tracker.get_slot("appointment_time"),
                                    tracker.get_slot("appointment_symptom")                    
                                )
                    return_list += [SlotSet("confirm_question", "appointment_confirm")]
                dispatcher.utter_message(text=res_msg)
                return return_list + [SlotSet("current_active_form", self.name()), 
                                      SlotSet("active_forms", list(set(tracker.get_slot("active_forms"))
                                    .union(set([self.name()]))) if tracker.get_slot("active_forms") else [self.name()])]
        
        if tracker.get_slot("appointment_confirm"):
            dispatcher.utter_message(text="Your appointment has been booked!")
            dispatcher.utter_message(text="{} will call you at {}"
                                .format(tracker.get_slot("appointment_doctor_name"), tracker.get_slot("appointment_time")))
            dispatcher.utter_message(text="Thank you!")
        else:
            dispatcher.utter_message(text="Thank you for using our service. Hope to see you soon!")
            
        return return_list + [SlotSet("appointment_doctor_name", None), SlotSet("appointment_symptom", None)
                                    ,SlotSet("appointment_time", None), SlotSet("appointment_day", None)
                                    ,SlotSet("confirm_question", None), SlotSet("appointment_confirm", None)] + [SlotSet("current_active_form", None), 
                                      SlotSet("active_forms", list(set(tracker.get_slot("active_forms"))
                                    .difference(set([self.name()]))) if tracker.get_slot("active_forms") else [])]
    
    def extract_appointment_time(self, tracker: Tracker):
        appointment_time = list(filter(lambda e: e.get("entity") == "time", tracker.latest_message.get("entities")))[0]
        log.info("appointment_time: {}".format(appointment_time))
         
class ActionInformDateTime(Action):
    def name(self) -> str:
        return "action_inform_date_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        appointment_time = tracker.get_slot("appointment_time")
        appointment_day = tracker.get_slot("appointment_day")
        
        log.info("action_inform_date_time -> appointment_time: {}, appointment_day: {}"
                 .format(appointment_time, appointment_day))

        if appointment_time == None or appointment_day == None:
            dispatcher.utter_message(text={"available_slots":"6:30\n7:00\n7:30"})
            return []
        return [FollowupAction("action_book_appointment")]

class ActionInformSymptom(Action):
    def name(self) -> str:
        return "action_inform_symptom"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        appointment_symptom = tracker.get_slot("appointment_symptom")
        log.info("action_inform_symptom -> symptom_desc: {}"
                 .format(appointment_symptom))
        current_active_form = tracker.get_slot("current_active_form")
        if current_active_form == "action_book_appointment":
            return [SlotSet("appointment_symptom", tracker.latest_message.get("text")), FollowupAction("action_book_appointment")]
        else:
            dispatcher.utter_message(text="Sorry to here that.")
            dispatcher.utter_message(text="I can help you to get a consultancy with our doctor")
            dispatcher.utter_message(text="would you like to book an appointment?")
            return [FollowupAction("action_listen"), SlotSet("confirm_question", "continue_with_appointment")] + [SlotSet("current_active_form", "action_book_appointment"), 
                                      SlotSet("active_forms", list(set(tracker.get_slot("active_forms"))
                                    .union(set(["action_book_appointment"]))) if tracker.get_slot("active_forms") else ["action_book_appointment"])]

class ActionInformDoctor(Action):
    def name(self) -> str:
        return "action_inform_doctor"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        action_inform_doctor = tracker.get_slot("appointment_doctor_name")
        log.info("action_inform_doctor -> action_inform_doctor: {}"
                 .format(action_inform_doctor))
        return [FollowupAction("action_book_appointment")]
    
    
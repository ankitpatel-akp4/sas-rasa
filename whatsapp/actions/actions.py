# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict
# from rasa_sdk.events import SlotSet


class ActionApplyLoan(Action):
    def name(self) -> str:
        return "action_apply_loan"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: dict) -> list:
        loan_type = tracker.get_slot('loan_type')
        amount = tracker.get_slot('amount')
        duration = tracker.get_slot('duration')
        name = tracker.get_slot('name')

        # Here you would typically call an external API to process the
        # loan application
        dispatcher.utter_message(text=f"Loan application submitted for\
                                 {name}: {loan_type} loan of {amount}\
                                 dollars for {duration}.")
        return []


class ActionLoanStatus(Action):
    def name(self) -> str:
        return "action_loan_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: dict) -> list:
        # Here you would typically call an external API to get the loan status
    
        dispatcher.utter_message(text="Your loan application is currently\
            being processed.")
        return []


class ActionLoanRepayment(Action):
    def name(self) -> str:
        return "action_loan_repayment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: dict) -> list:
        loan_type = tracker.get_slot('loan_type')
        amount = tracker.get_slot('amount')

        # Here you would typically call an external API to get repayment 
        # details
        dispatcher.utter_message(text=f"Repayment details for {loan_type} loan\
                                 of {amount} dollars.")
        return []


class ActionInterestRates(Action):
    def name(self) -> str:
        return "action_interest_rates"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict) -> list:
        loan_type = tracker.get_slot('loan_type')
        duration = tracker.get_slot('duration')

        # Here you would typically call an external API to get interest rates
        dispatcher.utter_message(text=f"The interest rate for a {loan_type}" +
                                 f"loan for {duration} is 5%.")
        return []

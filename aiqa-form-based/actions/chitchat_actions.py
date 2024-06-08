from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging

log = logging.getLogger(__name__)

faq_chitchat_dict: dict = {
    "faq/ask_aboutaiqa": "Aiqahealth is on a mission to resolve unequal access to healthcare in India. While India’s middle class, and above, in Metros have very good access to the best healthcare facilities, of the doctors and the hospitals, people in tier 2 and tier 3 cities and blue-collar workers in metros don’t have such luxury. This stems from both, the lack of affordability and dearth of good medical specialists serving in tier 2 and 3 cities. Hence, most patients, whether due to lack of affordability or lack of availability, are forced to seek health care from untrained and unqualified providers. aiqahealth products provides affordable continued care for the in tier 2 and tier 3 cities and also in metros.",
    "faq/ask_help": "As an AI model am trained to help you with doctor's appointments.",
}


class ActionChitchatAskName(Action):

    def name(self) -> Text:
        return "action_chitchat_ask_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="I am a bot.")

        return []

class ActionTriggerResponseSelector(Action):

    def name(self) -> Text:
        return "action_trigger_response_selector"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log.info("action_trigger_response_selector => intent: {}".format(tracker.latest_message.get("intent").get("full_retrieval_intent_name")))
        full_retrieval_intent_name = tracker.latest_message.get("intent").get("full_retrieval_intent_name")
        dispatcher.utter_message(text=faq_chitchat_dict.get(full_retrieval_intent_name))

        return []

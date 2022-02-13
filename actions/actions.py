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

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.db import service_comments, db_conn


class ActionAcknowledgeComment(Action):

    def name(self) -> Text:
        return "action_acknowledge_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if len(tracker.latest_message["entities"]) > 0:
            message = tracker.latest_message["text"]
            service = tracker.latest_message["entities"][0]["value"]
            print(service, message)

            insert_instruction = service_comments.insert().values(message=message, service=service)
            db_conn.execute(insert_instruction)

        dispatcher.utter_message(response="utter_acknowledge_comment")

        return []

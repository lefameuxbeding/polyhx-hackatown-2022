# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.executor import CollectingDispatcher

from actions.db import service_comments, db_conn
from actions.sentiment import sample_analyze_sentiment


class ActionAcknowledgeComment(Action):

    def name(self) -> Text:
        return "action_acknowledge_comment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if len(tracker.latest_message["entities"]) > 0:
            message = tracker.latest_message["text"]
            service = tracker.latest_message["entities"][0]["value"]

            sentiment = sample_analyze_sentiment(message)
            logger.info(f"[{service}] <- {sentiment}: {message}")

            insert_instruction = service_comments.insert().values(message=message, service=service, sentiment=sentiment)
            db_conn.execute(insert_instruction)

        dispatcher.utter_message(response="utter_acknowledge_comment")

        return []

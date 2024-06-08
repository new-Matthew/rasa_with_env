# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class Action_say_phone(Action):

     def name(self) -> Text:
         return "action_say_phone"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         phone = tracker.get_slot("phone")

         if not phone:
             dispatcher.utter_message(text="Desculpe nao sei seu numero de telefone")
         else:
             dispatcher.utter_message(text=f"seu número de telefone é: {phone}")

         return []
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSayData(Action):

     def name(self) -> Text:
         return "action_travel_info"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         origin_country = tracker.get_slot("origin_country")
         destiny_country = tracker.get_slot("destiny_country")
#         origin_coin = tracker.get_slot("money_to_convert")

         dispatcher.utter_message(text=f"seu país de origem é {origin_country}, seu país de destino é {destiny_country}, com @origin_coin você consegue comprar @destiny_coin (sem taxas de câmbio inclusas) ")

         return []
     
#     if not phone:
#             dispatcher.utter_message(text="Desculpe nao sei seu numero de telefone")
#         else:
#             dispatcher.utter_message(text=f"seu número de telefone é: {phone}")
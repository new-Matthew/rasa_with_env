# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset

import requests
import json


from rasa_sdk.events import AllSlotsReset, SlotSet

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionJoke(Action):
  def name(self):
    return "action_joke"

  def run(sself, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
    request = requests.get('https://v2.jokeapi.dev/joke/Any?lang=pt').json()  # make an api call
    #pergunta = request[0]['setup']  # extract a joke from returned json response
    pergunta = request['setup']
    resposta = request['delivery']
    print(request)
    print(pergunta)
    print(resposta)
    dispatcher.utter_message(text=pergunta)  # send the message back to the user
    dispatcher.utter_message(text=resposta)
    print("\n\n\n")
    print(request)
    return []
    
class ActionTravelInfo(Action):

    def name(self) -> Text:
        return "action_travel_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Obtém os valores dos slots
            origin_country = tracker.get_slot("origin_country")
            destiny_country = tracker.get_slot("destiny_country")
            origin_coin_to_convert = tracker.get_slot("origin_coin_to_convert")

            if not origin_country or not destiny_country or not origin_coin_to_convert:
                dispatcher.utter_message(text="Por favor, forneça todos os detalhes necessários: país de origem, país de destino e valor em moeda de origem.")
                return []

            # Mapear país de destino para a moeda correspondente
            currency_mapping = {
                "EUA": "USD",
                "França": "EUR",
                "Japão": "JPY",
                "Equador": "USD",
                "México": "MXN",
                "Espanha": "EUR",
                "Portugal": "EUR",
                "Brasil": "BRL"
            }

            # Verifica se o país de destino está no mapeamento
            if destiny_country not in currency_mapping:
                dispatcher.utter_message(text=f"Desculpe, não tenho informações de câmbio para {destiny_country}.")
                return [AllSlotsReset(), SlotSet("requested_slot")]

            # Obtém a moeda do país de destino
            destiny_currency = currency_mapping[destiny_country]

            # URL da API para conversão de moeda
            url = f'https://economia.awesomeapi.com.br/last/BRL-{destiny_currency}'

            # Função para obter a taxa de câmbio
            def get_exchange_rate(url):
                response = requests.get(url)
                response.raise_for_status()  # Levanta uma exceção para respostas HTTP não bem-sucedidas
                data = response.json()
                return float(next(iter(data.values()))['bid'])

            # Obter a taxa de câmbio
            rate = get_exchange_rate(url)

            # Converter o valor em BRL para a moeda do país de destino
            value_in_brl = float(origin_coin_to_convert)
            value_in_destiny_currency = value_in_brl * rate

            # Armazenar o resultado na variável destiny_coin
            destiny_coin = f"{value_in_destiny_currency:.2f} {destiny_currency}"

            # Mensagem de saída
            output_message = (
                f"Seu país de origem é {origin_country}, seu país de destino é {destiny_country}. "
                f"Com {value_in_brl} BRL, você consegue comprar {destiny_coin} (sem taxas de câmbio inclusas)."
            )

            # Envia a mensagem de volta para o usuário
            dispatcher.utter_message(text=output_message)

            # Reseta os slots e define o slot solicitado
            return [AllSlotsReset(), SlotSet("requested_slot")]

        except requests.RequestException as e:
            dispatcher.utter_message(text="Desculpe, houve um problema ao acessar o serviço de câmbio. Tente novamente mais tarde.")
            return []

        except ValueError:
            dispatcher.utter_message(text="Por favor, forneça um valor numérico válido para conversão.")
            return []

        except Exception as e:
            dispatcher.utter_message(text=f"Ocorreu um erro inesperado: {e}")
            return []


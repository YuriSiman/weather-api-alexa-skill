# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Em qual cidade você gostaria de pedalar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class GetWeatherIntentHandler(AbstractRequestHandler):
    """Handler for Get Weather Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetWeatherIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        city = slots['city'].value
        speak_output = ''
        lang = '&lang=pt_br'
        api_address = "https://api.openweathermap.org/data/2.5/weather?appid=52128bf6293eea0a463151d60d483d46&q="
        url = api_address + city + lang
        json_data = requests.get(url).json()
        id = json_data['weather'][0]['id']
        description = json_data['weather'][0]['description']
        temp_json = json_data['main']['temp']
        temp = round(temp_json - 273.15)
        humidity = json_data['main']['humidity']
        if (id == 800):
            description = "céu limpo"
        elif (id >= 200 and id <= 232):
            description = "trovoada"
        elif (id >= 300 and id <= 321):
            description = "chuvisco"
        elif (id >= 500 and id <= 531):
            description = "chuva"
        elif (id >= 600 and id <= 622):
            description = "neve"    
        elif (id >= 801 and id <= 804):
            description = "nuvens"
        if (temp < 15 and (id >= 800 and id <= 804)):
            speak_output = "Hmm... O clima está frio em {city} para pedalar, a temperatura é de {temp}° e o tempo está com {description}, a humidade está em {humidity}%.".format(city=city,description=description,temp=temp,humidity=humidity)
        elif (temp < 15 and (id >= 200 and id <= 622)):
            speak_output = "O tempo não está nada bom para pedalar em {city}, está frio com uma temperatura de {temp}° e o tempo está com {description}, a humidade está em {humidity}%.".format(city=city,description=description,temp=temp,humidity=humidity)
        elif (temp < 15):
            speak_output = "Hmm... O clima está frio em {city} para pedalar, a temperatura é de {temp}° e o tempo está com {description}, a humidade está em {humidity}%.".format(city=city,description=description,temp=temp,humidity=humidity)
        if (temp > 15 and (id >= 800 and id <= 804)):
            speak_output = "Está calor em {city} com um clima bom para pedalar, a temperatura é de {temp}° e o tempo está com {description}, a humidade está em {humidity}%.".format(city=city,description=description,temp=temp,humidity=humidity)
        elif (temp > 15 and (id >= 200 and id <= 622)):
            speak_output = "Está calor em {city}, porém o tempo não está nada bom para pedalar, a temperatura é de {temp}°, mas o tempo está com {description}, a humidade está em {humidity}%.".format(city=city,description=description,temp=temp,humidity=humidity)
        elif (temp > 15):
            speak_output = "Está calor em {city} com um clima bom para pedalar, a temperatura é de {temp}° e o tempo está com {description}, a humidade está em {humidity}%.".format(city=city,description=description,temp=temp,humidity=humidity)
        
        repromptOutput = " Você quer saber o tempo novamente de outra cidade?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(repromptOutput)
                .response
        )


class ThanksIntentHandler(AbstractRequestHandler):
    """Handler for Thanks Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ThanksIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Por nada! Precisando, é só chamar."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Você pode dizer olá para mim! Como posso ajudar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Até logo!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hum, não tenho certeza. Você pode dizer Olá ou Ajuda. O que você gostaria de fazer?"
        reprompt = "Eu não entendi isso. Com o que posso ajudar?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, não entendi o que você pediu. Por favor, tente novamente."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetWeatherIntentHandler())
sb.add_request_handler(ThanksIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
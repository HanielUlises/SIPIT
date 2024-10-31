# -*- coding: utf-8 -*-

import logging
import requests
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuración de Notion
NOTION_API_TOKEN = "tu_token_de_notion"
NOTION_VERSION = "2022-06-28"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}


# Handlers de solicitud
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler para LaunchRequest de Alexa."""
    def can_handle(self, handler_input):
        if handler_input.request_envelope.request is None:
            logger.error("Request is None")
            return False
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")
        speech = "Bienvenido a la Skill de Notion para Alexa. ¿En qué puedo ayudarte?"
        handler_input.response_builder.speak(speech).set_should_end_session(False)
        return handler_input.response_builder.response


class ConsultarPaginaIntentHandler(AbstractRequestHandler):
    """Handler para consultar una página en Notion."""
    def can_handle(self, handler_input):
        return is_intent_name("ConsultarPaginaIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In ConsultarPaginaIntentHandler")
        try:
            pagina_id = handler_input.request_envelope.request.intent.slots["paginaid"].value
            url = f"https://api.notion.com/v1/pages/{pagina_id}"
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            page_data = response.json()
            speech_text = f"La página con ID {pagina_id} tiene el título: {page_data['properties']['title']['title'][0]['text']['content']}."
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                speech_text = f"No encontré la página con ID {pagina_id}. Verifica el número e intenta de nuevo."
            else:
                speech_text = "Hubo un problema al consultar la página. Por favor intenta nuevamente más tarde."
        except Exception as e:
            logger.error("Error al consultar la página: %s", e)
            speech_text = "Ocurrió un error inesperado al consultar la página."
        
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class CrearPaginaIntentHandler(AbstractRequestHandler):
    """Handler para crear una nueva página en Notion."""
    def can_handle(self, handler_input):
        return is_intent_name("CrearPaginaIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In CrearPaginaIntentHandler")
        try:
            titulo = handler_input.request_envelope.request.intent.slots["title"].value
            data = {
                "parent": {"database_id": "tu_database_id"},
                "properties": {
                    "title": {
                        "title": [
                            {
                                "type": "text",
                                "text": {"content": titulo}
                            }
                        ]
                    }
                }
            }
            url = "https://api.notion.com/v1/pages"
            response = requests.post(url, headers=HEADERS, json=data)
            response.raise_for_status()
            page_data = response.json()
            speech_text = f"Se ha creado la página con ID {page_data['id']}."
        except requests.exceptions.HTTPError:
            speech_text = "No pude crear la página en Notion. Asegúrate de tener los permisos necesarios."
        except Exception as e:
            logger.error("Error al crear la página: %s", e)
            speech_text = "Hubo un error inesperado al crear la página. Intenta nuevamente."
        
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler para FallbackIntent."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Lo siento, no puedo ayudarte con eso. Intenta decir otra cosa."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler para HelpIntent."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In HelpIntentHandler")
        speech = "Esta es la skill de Notion. Puedes pedirme que consulte o cree páginas."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Handler para Cancel y Stop intents."""
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In ExitIntentHandler")
        handler_input.response_builder.speak("Adiós").set_should_end_session(True)
        return handler_input.response_builder.response




# Interceptores para registrar solicitudes y respuestas
class RequestLogger(AbstractRequestInterceptor):
    def process(self, handler_input):
        logger.info("Request: %s", handler_input.request_envelope)


class ResponseLogger(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        logger.info("Response: %s", response)



# Configuración de Skill Builder y registro de handlers e interceptores
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ConsultarPaginaIntentHandler())
sb.add_request_handler(CrearPaginaIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Exponer el handler de Lambda
lambda_handler = sb.lambda_handler()
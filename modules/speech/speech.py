import logging
import os

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# En esta lista, si bien es de alcance global, será usada para el
# manejo de las transcripciones y su tratamiento
transcriptions = []


class LaunchRequestHandler(AbstractRequestHandler):
    """Maneja LaunchRequest."""
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Hola, bienvenido a SIPIT. Di 'Iniciar' seguido de lo que deseas dictar. "
            "Cuando termines, di 'Genera la minuta'."
        )
        return (
            handler_input.response_builder
            .speak(speak_output)
            .reprompt(speak_output)
            .response
        )


class TranscribeIntentHandler(AbstractRequestHandler):
    """Maneja TranscribeIntent."""
    def can_handle(self, handler_input):
        return is_intent_name("TranscribeIntent")(handler_input)

    def handle(self, handler_input):
        global transcriptions

        user_input = handler_input.request_envelope.request.intent.slots["UserInput"].value
        transcriptions.append(user_input)

        word_count = len(" ".join(transcriptions).split())
        if word_count >= 1000:
            speak_output = (
                "Has alcanzado el límite de 1000 palabras. Por favor, di 'Genera la minuta' para obtener la minuta."
            )
        else:
            speak_output = f"He registrado tu minuta. Hasta ahora tienes {word_count} palabras. ¿Algo más?"
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .reprompt("¿Algo más que desees dictar?")
            .response
        )


class GenerateSummaryIntentHandler(AbstractRequestHandler):
    """Maneja GenerateSummaryIntent."""
    def can_handle(self, handler_input):
        return is_intent_name("GenerateSummaryIntent")(handler_input)

    def handle(self, handler_input):
        global transcriptions
        # Recuperamos la información
        if not transcriptions:
            speak_output = "No has dictado nada. Por favor, di algo para transcribir."
            return handler_input.response_builder.speak(speak_output).response
        # Tratamos la información y la guardamos
        full_text = " ".join(transcriptions)
        transcriptions = []

        file_path = "/tmp/transcription.txt"

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(full_text)
            logger.info(f"Archivo guardado en: {file_path}")
            speak_output = "El archivo con tu resumen ha sido generado. Puedes revisarlo en el servidor."
        except Exception as e:
            logger.error(f"Error al guardar el archivo: {e}")
            speak_output = "Hubo un problema al generar el archivo. Intenta nuevamente."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .with_simple_card("Resumen Generado", f"Archivo guardado en: {file_path}")
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Maneja HelpIntent."""
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Hola, bienvenido a SIPIT. Di 'Iniciar' seguido de lo que deseas dictar. "
            "Cuando termines, di 'Genera la minuta'."
        )
        return (
            handler_input.response_builder
            .speak(speak_output)
            .reprompt(speak_output)
            .response
        )


class CancelAndStopIntentHandler(AbstractRequestHandler):
    """Maneja Cancel y Stop intents."""
    def can_handle(self, handler_input):
        return (
            is_intent_name("AMAZON.CancelIntent")(handler_input) or
            is_intent_name("AMAZON.StopIntent")(handler_input)
        )

    def handle(self, handler_input):
        speak_output = "Adiós, espero haberte ayudado."
        return handler_input.response_builder.speak(speak_output).response


class ErrorHandler(AbstractExceptionHandler):
    """Maneja errores genéricos."""
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception)
        speak_output = "Lo siento, ocurrió un error. Intenta nuevamente."
        return (
            handler_input.response_builder
            .speak(speak_output)
            .reprompt("Intenta nuevamente.")
            .response
        )


# Configuración de la skill
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TranscribeIntentHandler())
sb.add_request_handler(GenerateSummaryIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(ErrorHandler())

lambda_handler = sb.lambda_handler()

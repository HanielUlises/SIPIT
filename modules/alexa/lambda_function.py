# -*- coding: utf-8 -*-

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractResponseInterceptor, AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type
#from ask_sdk_model import Response
import requests
import json
from s3_bucket import subirAS3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

transcriptions = []

class ComandosNotionIntentHandler(AbstractRequestHandler):
    """Handler para crear tareas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("ComandosNotionIntent")(handler_input) and
                'texto' in handler_input.request_envelope.request.intent.slots and
                handler_input.request_envelope.request.intent.slots['texto'].value)

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            url = "https://sipit-web.onrender.com/comandos/?texto="+texto

            respuesta = requests.post(url) 
            
            if respuesta.status_code == 200:
                response_data = respuesta.json()  
                respuesta_texto = response_data.get("respuesta")
                
                speech_text = f"La tarea se creó con éxito en Notion. Respuesta del servidor: {respuesta_texto}"
            else:
                speech_text = f"Error: {respuesta.status_code}: No se pudo crear la tarea. {respuesta_texto}"
                
        except Exception as e:
            logger.error(f"Error al crear tarea: {str(e)}")
            ab = f"Error al crear tarea: {str(e)}"
            speech_text = ab + " Hubo un error al crear la tarea. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response


class ComandosNotionIntentHandler(AbstractRequestHandler):
    """Handler para crear tareas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("ComandosNotionIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            url = "https://sipit-web.onrender.com/comandos/?texto=" + texto

            respuesta = requests.post(url) 
            
            if respuesta.status_code == 200:
                try:
                    response_data = respuesta.json()  
                    respuesta_texto = response_data.get("respuesta", "Respuesta no encontrada.")
                except ValueError:
                    respuesta_texto = respuesta.text

                speech_text = f"La tarea se creó con éxito en Notion. Respuesta del servidor: {respuesta_texto}"
            else:
                respuesta_texto = f"Error: {respuesta.status_code}: No se pudo crear la tarea."
                speech_text = respuesta_texto

        except Exception as e:
            logger.error(f"Error al crear tarea: {str(e)}")
            ab = f"Error al crear tarea: {str(e)}"
            speech_text = ab + " Hubo un error al crear la tarea. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response

        
# Handlers de solicitud
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler para LaunchRequest de Alexa."""
    def can_handle(self, handler_input):
        request = handler_input.request_envelope.request
        return request is not None and is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")
        speech = "Bienvenido a la Skill de Notion para Alexa. ¿En qué puedo ayudarte?"
        handler_input.response_builder.speak(speech).set_should_end_session(False)
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

#Handlers para comandos de notion
class TranscribeIntentHandler(AbstractRequestHandler):
    """Maneja TranscribeIntent."""
    def can_handle(self, handler_input):
        return is_intent_name("TranscribeIntent")(handler_input)

    def handle(self, handler_input):
        global transcriptions

        try:
            user_input = handler_input.request_envelope.request.intent.slots["UserInput"].value
        except KeyError:
            user_input = None

        if user_input:
            transcriptions.append(user_input)

            word_count = len(" ".join(transcriptions).split())
            if word_count >= 1000:
                speak_output = (
                    "Has alcanzado el límite de 1000 palabras. Por favor, di 'Genera la minuta' para obtener la minuta."
                )
            else:
                speak_output = f"He registrado tu minuta. Hasta ahora tienes {word_count} palabras. ¿Algo más?"
        else:
            speak_output = "No se recibió un texto válido para transcribir."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("¿Algo más que desees dictar?")
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
        nombre_bucket =  "sipit-transcriptions"
        llave_archivo = "transcriptions/transcription.txt"

        try:
            
            url = "https://sipit-web.onrender.com/minutatxt/?texto_minuta="+full_text
            url2 = "https://sipit-web.onrender.com/minuta_resumen/?texto_minuta="+full_text
            respuesta = requests.post(url) 
            respuesta2 = requests.post(url2)
            
            if respuesta.status_code == 200 or respuesta2.status_code == 200:
                response_data = respuesta.json()  
                response_data2 = respuesta2.json()
                
                speak_output = "El sistema recibió correctamente la minuta"
            else:
                speak_output = "Ocurrió un problema al recibir la minuta."

            #with open(file_path, "w", encoding="utf-8") as file:
            #    file.write(full_text)
            #logger.info(f"Archivo guardado en: {file_path}")
            #speak_output = "El archivo con tu resumen ha sido generado. Puedes revisarlo en el servidor."

            #Aqui se subira el archivo a S3
            #if subirAS3(nombre_bucket,file_path,llave_archivo):
            #    speak_output = "El archivo con tu resumen se ha registrado exitosamente a S3."
            #else:
            #    speak_output = "El archivo fue generado, pero no se pudo subir"

        except Exception as e:
            logger.error(f"Error al guardar la minuta: {e}")
            speak_output = "Hubo un problema al generar la minuta. Intenta nuevamente."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )

def lambda_handler(event, context):
    # Configuración del bucket y archivo
    bucket_name = "sipit-transcriptions"  # Cambia esto por el nombre de tu bucket
    file_path = "/tmp/transcription.txt"  # Ruta del archivo generado en Lambda
    file_key = "transcriptions/transcription.txt"  # Ruta dentro del bucket

    # Generar un archivo temporal (esto es un ejemplo; tú ya lo tienes generado)
    with open(file_path, "w") as f:
        f.write("Este es un archivo generado desde Lambda.")

    # Subir el archivo al bucket
    resultado = subirAS3(bucket_name, file_path, file_key)
    if resultado:
        return {
            "statusCode": 200,
            "body": f"Archivo subido exitosamente a {bucket_name}/{file_key}"
        }
    else:
        return {
            "statusCode": 500,
            "body": "Hubo un error al subir el archivo al bucket S3."
        }

# Interceptores para registrar solicitudes y respuestas
class RequestLogger(AbstractRequestInterceptor):
    def process(self, handler_input):
        logger.info("Request: %s", handler_input.request_envelope)


class ResponseLogger(AbstractResponseInterceptor):
    def process(self, handler_input, response):
        logger.info("Response: %s", response)

# Configuración de Skill Builder y registro de handlers e interceptores
sb = SkillBuilder()
sb.add_request_handler(ComandosNotionIntentHandler())  

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(ExitIntentHandler())

sb.add_request_handler(TranscribeIntentHandler())
sb.add_request_handler(GenerateSummaryIntentHandler())



sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()
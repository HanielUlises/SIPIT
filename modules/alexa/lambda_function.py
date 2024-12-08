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

class CrearTareaHandler(AbstractRequestHandler):
    """Handler para crear tareas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("CrearTareaIntent")(handler_input) and
            handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            
            url = "https://sipit-web.onrender.com/comandos/?texto="+texto
    
            respuesta = requests.post(url)

            # Verificar si la solicitud fue exitosa y mostrar la respuesta
            if respuesta.status_code == 200:
                speech_text = "El proyecto se creó con éxito en Notion."
            else:
                for respuest in respuesta :
                    cuak =f"cuak{respuest}"
                
                speech_text = f"Error:  {respuesta.status_code}: No se pudo crear la tarea."+cuak
                
        except Exception as e:
            logger.error(f"Error al crear tarea: {str(e)}")
            ab = f"Error al crear tarea: {str(e)}"
            speech_text = ab+"Hubo un error al crear la tarea. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response


class CrearProyectoHandler(AbstractRequestHandler):
    """Handler para crear proyectos en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("CrearProyectoIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.CrearProyecto(texto)
            
            if respuesta.status_code == 200:
                speech_text = "El proyecto se creó con éxito en Notion."
            else:
                speech_text = f"Error {respuesta.status_code}: No se pudo crear el proyecto."
                
        except Exception as e:
            logger.error(f"Error al crear proyecto: {str(e)}")
            speech_text = "Hubo un error al crear el proyecto. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class CrearSprintHandler(AbstractRequestHandler):
    """Handler para crear sprints en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("CrearSprintIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.crear_tarea(texto)
            
            if respuesta.status_code == 200:
                speech_text = "El sprint se creó con éxito en Notion."
            else:
                speech_text = f"Error {respuesta.status_code}: No se pudo crear el sprint."
                
        except Exception as e:
            logger.error(f"Error al crear sprint: {str(e)}")
            speech_text = "Hubo un error al crear el sprint. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response

class CrearMinutaHandler(AbstractRequestHandler):
    """Handler para crear minutas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("CrearMinutaIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.crear_minuta(texto)
            
            if respuesta.status_code == 200:
                speech_text = "La minuta se creó con éxito en Notion."
            else:
                speech_text = f"Error {respuesta.status_code}: No se pudo crear la minuta."
                
        except Exception as e:
            logger.error(f"Error al crear la minuta: {str(e)}")
            speech_text = "Hubo un error al crear la minuta. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response

class ConsultarTareasHandler(AbstractRequestHandler):
    """Handler para consultar tareas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("ConsultarTareasIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_tareas(texto)
            
            speech_text = respuesta
            # Guardar datos en archivo JSON (opcional)
            #with open("db.json", "w") as fd:
            #    json.dump(datos, fd, sort_keys=False, indent=4)
            #print("Aqui")
            # Definir el prompt para interpretar las tareas
                
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class ConsultarProyectoHandler(AbstractRequestHandler):
    """Handler para consultar proyectos en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("ConsultarProyectoIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_PROYECTOS(texto)
            
            speech_text = respuesta
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class ConsultarSprintHandler(AbstractRequestHandler):
    """Handler para consultar proyectos en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("ConsultarSprintIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_sprints(texto)
            
            speech_text = respuesta
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class ConsultarMinutaHandler(AbstractRequestHandler):
    """Handler para consultar proyectos en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("ConsultarSprintIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_tareas(texto)
            
            speech_text = respuesta
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class EliminarProyectoHandler(AbstractRequestHandler):
    """Handler para eliminar proyectos en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("EliminarProyectoIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_tareas(texto)
            speech_text = respuesta
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class EliminarTareaHandler(AbstractRequestHandler):
    """Handler para eliminar proyectos en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("EliminarTareaIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_tareas(texto)
            speech_text = respuesta
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class EliminarMinutaHandler(AbstractRequestHandler):
    """Handler para eliminar minuta en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("EliminarMinutaIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_tareas(texto)
            speech_text = respuesta
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    
class EliminarSprintHandler(AbstractRequestHandler):
    """Handler para eliminar sprint en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("EliminarSprintIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_tareas(texto)
            speech_text = respuesta
                
        except Exception as e:
            logger.error(f"Error al eliminar sprint: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response

#este no lo prueben    
class ActualizarTareaHandler(AbstractRequestHandler):
    """Handler para crear minutas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("CrearMinutaIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            respuesta = cN.consultar_tareas(texto)
            
            if respuesta.status_code == 200:
                speech_text = "La minuta se creó con éxito en Notion."
            else:
                speech_text = f"Error {respuesta.status_code}: No se pudo crear la minuta."
                
        except Exception as e:
            logger.error(f"Error al crear la minuta: {str(e)}")
            speech_text = "Hubo un error al crear la minuta. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response
    

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

#Handlers para comandos de notion
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
        nombre_bucket =  "sipit-transcriptions"
        llave_archivo = "transcriptions/transcription.txt"

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(full_text)
            logger.info(f"Archivo guardado en: {file_path}")
            #speak_output = "El archivo con tu resumen ha sido generado. Puedes revisarlo en el servidor."

            #Aqui se subira el archivo a S3
            if subirAS3(nombre_bucket,file_path,llave_archivo):
                speak_output = "El archivo con tu resumen ha sido subid exitosamente a S3."
            else:
                speak_output = "El archivo fue generado, pero no se pudo subir"

        except Exception as e:
            logger.error(f"Error al guardar el archivo: {e}")
            speak_output = "Hubo un problema al generar el archivo. Intenta nuevamente."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .with_simple_card("Resumen Generado", f"Archivo guardado en: {file_path}")
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

# Configuración de Skill Builder y registro de handlers e interceptores
sb = SkillBuilder()
sb.add_request_handler(CrearTareaHandler())   
sb.add_request_handler(LaunchRequestHandler()) 
sb.add_request_handler(CrearProyectoHandler())        
sb.add_request_handler(CrearSprintHandler())          
sb.add_request_handler(ConsultarTareasHandler())      
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(TranscribeIntentHandler())
sb.add_request_handler(GenerateSummaryIntentHandler())
sb.add_request_handler(CrearTareaHandler())
sb.add_request_handler(CrearMinutaHandler())
sb.add_request_handler(CrearProyectoHandler())
sb.add_request_handler(CrearSprintHandler())
sb.add_request_handler(ConsultarProyectoHandler())
sb.add_request_handler(ConsultarTareasHandler())
sb.add_request_handler(ConsultarSprintHandler())
sb.add_request_handler(ConsultarMinutaHandler())
sb.add_request_handler(EliminarProyectoHandler())
sb.add_request_handler(EliminarTareaHandler())
sb.add_request_handler(EliminarSprintHandler())
sb.add_request_handler(EliminarMinutaHandler())
sb.add_request_handler(ActualizarTareaHandler())


sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()
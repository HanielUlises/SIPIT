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
from langchain_groq import ChatGroq

model = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import requests
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuración de Notion
NOTION_API_TOKEN = "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"
ID_DATABASE = "1232595bac6f812d8674d1f4e4012af9"
URL_CREACION = "https://api.notion.com/v1/pages"
CABECERA = {
    "Authorization": f"Bearer {TOKEN_NOTION}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

# Constantes de datos
TITULAR = {
    "id": "notion%3A%2F%2Ftasks%2Fassign_property",
    "type": "people",
    "people": [
        {
            "object": "user",
            "id": "52530542-7f01-412e-a370-662a3cb775dc",
            "name": "Karina Santiago",
            "type": "person",
            "person": {
                "email": "asantiagom1802@alumno.ipn.mx"
            }
        }
    ]
}

# Comandos de Notion

def CrearTarea(texto):
    # Definir el prompt para extraer valores del texto de entrada
    promptc = ChatPromptTemplate.from_template("""
    Extrae el nombre de la tarea, la fecha de inicio, la fecha de conclusión, el nivel de prioridad y la descripción del siguiente comando:
    {texto}
    y que los valores tengan este formato: nombre="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor", resumen="valor".
    Devuelve estos datos como un diccionario JSON con las claves "nombre", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
    Unicamente devuelve el JSON. Sin comentarios ni explicación.
    """)

    # Extraer los datos necesarios con el modelo
    chainc = promptc | model | StrOutputParser()
    resultado_prompt = chainc.invoke({"texto": texto})
    datos_tarea = json.loads(resultado_prompt)

    # Definir los datos de la nueva entrada combinando los parámetros extraídos y las constantes
    nueva_entrada = {
        "parent": {"database_id": ID_DATABASE},
        "properties": {
            "Nombre de la tarea": {
                "title": [{"text": {"content": datos_tarea["nombre"]}}]
            },
            "Etiquetas": {
                "multi_select": ETIQUETAS
            },
            "Titular": TITULAR,
            "Estado": {
                "status": {"name": ESTADO}
            },
            "Fecha": {
                "date": {
                    "start": datos_tarea["fecha_inicio"],
                    "end": datos_tarea["fecha_fin"]
                }
            },
            "Proyecto": {
                "id": "notion%3A%2F%2Ftasks%2Ftask_to_project_relation",
                "type": "relation",
                "relation": [{"id": ID_PROYECTO}]
            },
            "Prioridad": {
                "select": {"name": datos_tarea["prioridad"]}
            },
            "Resumen": {
                "rich_text": [{"text": {"content": datos_tarea["resumen"]}}]
            }
        }
    }

    # Realizar la solicitud POST a la API de Notion para crear una nueva entrada
    respuesta = requests.post(URL_CREACION, headers=CABECERA, data=json.dumps(nueva_entrada))

    # Verificar si la solicitud fue exitosa y mostrar la respuesta
    if respuesta.status_code == 200:
        print("La tarea se creó con éxito en Notion.")
        #print(json.dumps(respuesta.json(), sort_keys=False, indent=4))
    else:
        print(f"Error {respuesta.status_code}: No se pudo crear la tarea.")
        print(json.dumps(respuesta.json(), sort_keys=False, indent=4))

# Ejemplo de uso
#texto = """SIPIT, crea una tarea con nombre "FUNCION MAESTRA", que tenga fecha de inicio "01-11-2024" y con una fecha de conclusión "15-11-2024",
#con un nivel de prioridad "Alta", con la descripción "Revisar y ajustar los puntos críticos del proyecto"."""
#CrearTarea(texto)

def CrearProyecto(texto):
    # Definir el prompt para extraer valores del texto de entrada
    promptc = ChatPromptTemplate.from_template("""
    Extrae el nombre del proyecto, la fecha de inicio, la fecha de conclusión y el nivel de prioridad del siguiente comando:
    {texto}
    y que los valores tengan este formato: nombre="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor".
    Devuelve estos datos como un diccionario JSON con las claves "nombre", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
    Unicamente devuelve el JSON. Sin comentarios ni explicación.
    """)

    # Extraer los datos necesarios con el modelo
    chainc = promptc | model | StrOutputParser()
    resultado_prompt = chainc.invoke({"texto": texto})
    print(resultado_prompt)
    datos_tarea = json.loads(resultado_prompt)

    # Definir los datos de la nueva entrada combinando los parámetros extraídos y las constantes
    nueva_entrada = {
        "parent": {"database_id": ID_DATABASE},
        "properties": {
            "Nombre del proyecto": {
                "title": [{"text": {"content": datos_tarea["nombre"]}}]
            },
            "Titular": TITULAR,
            "Estado": {
                "status": {"name": ESTADO}
            },
            "Fechas": {
                "date": {
                    "start": datos_tarea["fecha_inicio"],
                    "end": datos_tarea["fecha_fin"]
                }
            },
            "Prioridad": {
                "select": {"name": datos_tarea["prioridad"]}
            }
        }
    }

    # Realizar la solicitud POST a la API de Notion para crear una nueva entrada
    respuesta = requests.post(URL_CREACION, headers=CABECERA, data=json.dumps(nueva_entrada))

    # Verificar si la solicitud fue exitosa y mostrar la respuesta
    if respuesta.status_code == 200:
        print("El proyecto se creó con éxito en Notion.")
        #print(json.dumps(respuesta.json(), sort_keys=False, indent=4))
    else:
        print(f"Error {respuesta.status_code}: No se pudo crear la tarea.")
        print(json.dumps(respuesta.json(), sort_keys=False, indent=4))

# Ejemplo de uso
#texto = """SIPIT, crea un proyecto con nombre "YUJU", que tenga fecha de inicio "01-11-2024" y con una fecha de conclusión "15-11-2024",
#con un nivel de prioridad "Low""."""
#CrearProyecto(texto)


# Función principal para crear una nueva tarea en Notion
def CrearSprint(texto):
    # Definir el prompt para extraer valores del texto de entrada
    promptc = ChatPromptTemplate.from_template("""
    Extrae el nombre del sprint, la fecha de inicio y la fecha de conclusión del siguiente comando:
    {texto}
    y que los valores tengan este formato: nombre="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD".
    Devuelve estos datos como un diccionario JSON con las claves "nombre", "fecha_inicio" y "fecha_fin".
    Unicamente devuelve el JSON. Sin comentarios ni explicación.
    """)

    # Extraer los datos necesarios con el modelo
    chainc = promptc | model | StrOutputParser()
    resultado_prompt = chainc.invoke({"texto": texto})
    print(resultado_prompt)
    datos_tarea = json.loads(resultado_prompt)

    # Definir los datos de la nueva entrada combinando los parámetros extraídos y las constantes
    nueva_entrada = {
        "parent": {"database_id": ID_DATABASE},
        "properties": {
            "Nombre del Sprint": {
                "title": [{"text": {"content": datos_tarea["nombre"]}}]
            },
            "Fechas": {
                "date": {
                    "start": datos_tarea["fecha_inicio"],
                    "end": datos_tarea["fecha_fin"]
                }
            }
        }
    }

    # Realizar la solicitud POST a la API de Notion para crear una nueva entrada
    respuesta = requests.post(URL_CREACION, headers=CABECERA, data=json.dumps(nueva_entrada))

    # Verificar si la solicitud fue exitosa y mostrar la respuesta
    if respuesta.status_code == 200:
        print("El SPRINT se creó con éxito en Notion.")
        #print(json.dumps(respuesta.json(), sort_keys=False, indent=4))
    else:
        print(f"Error {respuesta.status_code}: No se pudo crear la tarea.")
        print(json.dumps(respuesta.json(), sort_keys=False, indent=4))

# Ejemplo de uso
#texto = """SIPIT, crea un Sprint con nombre "Sprint 5", que tenga fecha de inicio "01-11-2024" y con una fecha de conclusión "15-11-2024"."""
#CrearSprint(texto)


# Función principal para consultar y procesar tareas
def ConsultarTareas(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae la fecha con formato YYYY-MM-DD y el nivel de prioridad del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con las claves "prioridad", "fecha_inicio".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_consulta = json.loads(codigo)

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "1232595bac6f812d8674d1f4e4012af9"

    # Obtener datos desde Notion
    url_pregunta = f"https://api.notion.com/v1/databases/{id_database}/query"
    cabecera = {
        "Authorization": f"Bearer {token_notion}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    busqueda = {
        "page_size": 10,
        "filter": {
            "and": [
                {
                    "property": "Prioridad",
                    "select": {
                        "equals": datos_consulta["prioridad"]
                    }
                },
                {
                    "property": "Fecha",
                    "date": {
                        "on_or_after": datos_consulta["fecha_inicio"]
                    }
                }
            ]
        }
    }

    respuesta = requests.post(url_pregunta, headers=cabecera, data=json.dumps(busqueda))
    if respuesta.status_code == 200:
        print("Datos obtenidos con éxito")
    else:
        print(f"Error {respuesta.status_code}: No se pudo obtener los datos")

    datos = respuesta.json()

    # Guardar datos en archivo JSON (opcional)
    with open("db.json", "w") as fd:
        json.dump(datos, fd, sort_keys=False, indent=4)
    print("Aqui")
    # Definir el prompt para interpretar las tareas
    prompt_interpretar = ChatPromptTemplate.from_template(
        """
        interpreta: {text}. Solo dime el contenido que esta en la propiedad tittle de cada tarea.
        """
    )
    chain_interpretar = prompt_interpretar | model | StrOutputParser()
    interpretacion = chain_interpretar.invoke({"text": datos})

    return interpretacion

# Ejemplo de uso
#texto = "SIPIT, resume las tareas de el dia 01-11-2024 y con prioridad Alta"
#resultado = ConsultarTareas(texto)
#print(resultado)
class CrearTareaHandler(AbstractRequestHandler):
    """Handler para crear tareas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("CrearTareaIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            # Definir el prompt para extraer valores del texto de entrada
            promptc = ChatPromptTemplate.from_template("""
            Extrae el nombre de la tarea, la fecha de inicio, la fecha de conclusión, el nivel de prioridad y la descripción del siguiente comando:
            {texto}
            y que los valores tengan este formato: nombre="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor", resumen="valor".
            Devuelve estos datos como un diccionario JSON con las claves "nombre", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
            Unicamente devuelve el JSON. Sin comentarios ni explicación.
            """)

            # Extraer los datos necesarios con el modelo
            chainc = promptc | model | StrOutputParser()
            resultado_prompt = chainc.invoke({"texto": texto})
            datos_tarea = json.loads(resultado_prompt)

            # Definir los datos de la nueva entrada
            nueva_entrada = {
                "parent": {"database_id": ID_DATABASE},
                "properties": {
                    "Nombre de la tarea": {
                        "title": [{"text": {"content": datos_tarea["nombre"]}}]
                    },
                    "Etiquetas": {
                        "multi_select": ETIQUETAS
                    },
                    "Titular": TITULAR,
                    "Estado": {
                        "status": {"name": ESTADO}
                    },
                    "Fecha": {
                        "date": {
                            "start": datos_tarea["fecha_inicio"],
                            "end": datos_tarea["fecha_fin"]
                        }
                    },
                    "Proyecto": {
                        "id": "notion%3A%2F%2Ftasks%2Ftask_to_project_relation",
                        "type": "relation",
                        "relation": [{"id": ID_PROYECTO}]
                    },
                    "Prioridad": {
                        "select": {"name": datos_tarea["prioridad"]}
                    },
                    "Resumen": {
                        "rich_text": [{"text": {"content": datos_tarea["resumen"]}}]
                    }
                }
            }

            # Realizar la solicitud POST a la API de Notion
            respuesta = requests.post(URL_CREACION, headers=CABECERA, data=json.dumps(nueva_entrada))
            
            if respuesta.status_code == 200:
                speech_text = "La tarea se creó con éxito en Notion."
            else:
                speech_text = f"Error {respuesta.status_code}: No se pudo crear la tarea."
                
        except Exception as e:
            logger.error(f"Error al crear tarea: {str(e)}")
            speech_text = "Hubo un error al crear la tarea. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response


class CrearProyectoHandler(AbstractRequestHandler):
    """Handler para crear proyectos en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("CrearProyectoIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            # Definir el prompt para extraer valores
            promptc = ChatPromptTemplate.from_template("""
            Extrae el nombre del proyecto, la fecha de inicio, la fecha de conclusión y el nivel de prioridad del siguiente comando:
            {texto}
            y que los valores tengan este formato: nombre="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor".
            Devuelve estos datos como un diccionario JSON con las claves "nombre", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
            Unicamente devuelve el JSON. Sin comentarios ni explicación.
            """)

            # Extraer los datos necesarios
            chainc = promptc | model | StrOutputParser()
            resultado_prompt = chainc.invoke({"texto": texto})
            datos_tarea = json.loads(resultado_prompt)

            # Definir los datos del nuevo proyecto
            nueva_entrada = {
                "parent": {"database_id": ID_DATABASE},
                "properties": {
                    "Nombre del proyecto": {
                        "title": [{"text": {"content": datos_tarea["nombre"]}}]
                    },
                    "Titular": TITULAR,
                    "Estado": {
                        "status": {"name": ESTADO}
                    },
                    "Fechas": {
                        "date": {
                            "start": datos_tarea["fecha_inicio"],
                            "end": datos_tarea["fecha_fin"]
                        }
                    },
                    "Prioridad": {
                        "select": {"name": datos_tarea["prioridad"]}
                    }
                }
            }

            # Realizar la solicitud POST
            respuesta = requests.post(URL_CREACION, headers=CABECERA, data=json.dumps(nueva_entrada))
            
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
            # Definir el prompt para extraer valores
            promptc = ChatPromptTemplate.from_template("""
            Extrae el nombre del sprint, la fecha de inicio y la fecha de conclusión del siguiente comando:
            {texto}
            y que los valores tengan este formato: nombre="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD".
            Devuelve estos datos como un diccionario JSON con las claves "nombre", "fecha_inicio" y "fecha_fin".
            Unicamente devuelve el JSON. Sin comentarios ni explicación.
            """)

            # Extraer los datos necesarios
            chainc = promptc | model | StrOutputParser()
            resultado_prompt = chainc.invoke({"texto": texto})
            datos_tarea = json.loads(resultado_prompt)

            # Definir los datos del nuevo sprint
            nueva_entrada = {
                "parent": {"database_id": ID_DATABASE},
                "properties": {
                    "Nombre del Sprint": {
                        "title": [{"text": {"content": datos_tarea["nombre"]}}]
                    },
                    "Fechas": {
                        "date": {
                            "start": datos_tarea["fecha_inicio"],
                            "end": datos_tarea["fecha_fin"]
                        }
                    }
                }
            }

            # Realizar la solicitud POST
            respuesta = requests.post(URL_CREACION, headers=CABECERA, data=json.dumps(nueva_entrada))
            
            if respuesta.status_code == 200:
                speech_text = "El sprint se creó con éxito en Notion."
            else:
                speech_text = f"Error {respuesta.status_code}: No se pudo crear el sprint."
                
        except Exception as e:
            logger.error(f"Error al crear sprint: {str(e)}")
            speech_text = "Hubo un error al crear el sprint. Por favor, inténtalo de nuevo."

        return handler_input.response_builder.speak(speech_text).response


class ConsultarTareasHandler(AbstractRequestHandler):
    """Handler para consultar tareas en Notion."""
    def can_handle(self, handler_input):
        return (is_intent_name("ConsultarTareasIntent")(handler_input) and
                handler_input.request_envelope.request.intent.slots.get('texto'))

    def handle(self, handler_input):
        try:
            texto = handler_input.request_envelope.request.intent.slots['texto'].value
            # Define el prompt para extraer valores
            prompt_extract = ChatPromptTemplate.from_template(
                """
                Extrae la fecha con formato YYYY-MM-DD y el nivel de prioridad del comando:
                {texto}
                Devuelve estos datos como un diccionario JSON con las claves "prioridad", "fecha_inicio".
                Unicamente devuelve el JSON. Sin comentarios ni explicación.
                """
            )

            # Genera código con valores extraídos
            valores_extraidos = prompt_extract | model | StrOutputParser()
            codigo = valores_extraidos.invoke({"texto": texto})
            datos_consulta = json.loads(codigo)

            # Configurar la consulta
            busqueda = {
                "page_size": 10,
                "filter": {
                    "and": [
                        {
                            "property": "Prioridad",
                            "select": {
                                "equals": datos_consulta["prioridad"]
                            }
                        },
                        {
                            "property": "Fecha",
                            "date": {
                                "on_or_after": datos_consulta["fecha_inicio"]
                            }
                        }
                    ]
                }
            }

            # Realizar la consulta
            respuesta = requests.post(
                f"https://api.notion.com/v1/databases/{ID_DATABASE}/query",
                headers=CABECERA,
                data=json.dumps(busqueda)
            )
            
            if respuesta.status_code == 200:
                datos = respuesta.json()
                
                # Definir el prompt para interpretar las tareas
                prompt_interpretar = ChatPromptTemplate.from_template(
                    """
                    interpreta: {text}. Solo dime el contenido que esta en la propiedad tittle de cada tarea.
                    """
                )
                chain_interpretar = prompt_interpretar | model | StrOutputParser()
                interpretacion = chain_interpretar.invoke({"text": datos})
                
                speech_text = f"Las tareas encontradas son: {interpretacion}"
            else:
                speech_text = f"Error {respuesta.status_code}: No se pudieron consultar las tareas."
                
        except Exception as e:
            logger.error(f"Error al consultar tareas: {str(e)}")
            speech_text = "Hubo un error al consultar las tareas. Por favor, inténtalo de nuevo."

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
        # Slot: Nombre

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

#Handlers para comandos de notion

# Handler para crear una tarea
class CrearTareaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "CrearTareaIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = CrearTarea(texto)  # Llama a tu función CrearTarea
        speech_text = "La tarea ha sido creada." if resultado is None else f"Error al crear la tarea: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response

# Handler para consultar tareas
class ConsultarTareasIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "ConsultarTareasIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = ConsultarTareas(texto)  # Llama a tu función ConsultarTareas
        speech_text = f"Las tareas consultadas son: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response

# Configuración de Skill Builder y registro de handlers e interceptores
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ConsultarPaginaIntentHandler())
sb.add_request_handler(CrearPaginaIntentHandler())
sb.add_request_handler(CrearTareaHandler())           
sb.add_request_handler(CrearProyectoHandler())        
sb.add_request_handler(CrearSprintHandler())          
sb.add_request_handler(ConsultarTareasHandler())      
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())


sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Exponer el handler de Lambda
lambda_handler = sb.lambda_handler()

from flask import Flask, request, jsonify
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
# from ask_sdk_model import Response
import requests

app = Flask(__name__)
# Skill Builder de Alexa
sb = SkillBuilder()

# Token de Notion y la versión de la API que vamos a utilizar.
# El es la cadena de caracteres única que autentica a nuestra aplicación ante la API de Notion.
# Este token se genera al crear una integración en el sitio de desarrolladores de Notion!!
NOTION_API_TOKEN = "tu_token_de_notion"
NOTION_VERSION = "2022-06-28"                       # Versión más reciente de la API, según
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}

@app.route("/", methods=["POST"])
def invoke_skill():
    """
    Endpoint que invoca el skill de Alexa. 
    Este es el punto de entrada donde Alexa envía las solicitudes.
    """
    try:
        skill_response = sb.create().invoke(request.get_json())
        return jsonify(skill_response)
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado. Por favor intenta nuevamente."}), 500

@sb.request_handler(can_handle_func=lambda input: input.request_envelope.request.type == "LaunchRequest")
def launch_request_handler(handler_input: HandlerInput):
    """
    Maneja la solicitud de lanzamiento del skill. 
    Se ejecuta cuando el usuario inicia la skill en Alexa.
    """
    speech_text = "Bienvenido a la Skill de Notion para Alexa. ¿En qué puedo ayudarte?"
    return handler_input.response_builder.speak(speech_text).set_should_end_session(False).response

@sb.request_handler(can_handle_func=lambda input: input.request_envelope.request.intent.name == "CrearPaginaIntent")
def crear_pagina_handler(handler_input: HandlerInput):
    """
    Maneja la intención de crear una nueva página en Notion.
    Esta función se invoca cuando el usuario habla con Alexa y solicita crear una nueva página en Notion utilizando una frase adecuada.

    Proceso de interacción:
    1. El usuario se dirige a Alexa y dice una frase que activa la intención de creación de página. Por ejemplo:
       - "Alexa, crea una página llamada [Título de la nueva página]."
       - "Alexa, añade una nueva página titulada [Título de la nueva página]."
    2. Alexa reconoce la solicitud y activa la intención CrearPaginaIntent.
    3. Se envía una solicitud a la API de Notion para crear la página en la base de datos especificada.
    5. Una vez que la página es creada, Alexa responde al usuario con un mensaje confirmando que la nueva página ha sido creada con éxito.

    """
    try:
        # Extracción del título de la nueva página desde la solicitud
        titulo = handler_input.request_envelope.request.intent.slots["titulo"].value
        data = {
            # Hay que ajustar el ID de la BD
            # Desde luego que la base de datos es una base
            # de datos de Notion, es decir, una colección de páginas

            # Si tenemos la URL de la BD
            # https://www.notion.so/workspace_name/Proyectos-abcde7872783782
            # el ID entonces es: abcde7872783782
            "parent": {"database_id": "-"},
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
        # IMPORTANTE
        # URL para crear una nueva página en Notion
        url = "https://api.notion.com/v1/pages"
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        page_data = response.json()
        # La página fue creada
        speech_text = f"Se ha creado la página con ID {page_data['id']}."
    except requests.exceptions.HTTPError:
        speech_text = "No pude crear la página en Notion. Asegúrate de tener los permisos necesarios."
    except Exception:
        speech_text = "Hubo un error inesperado al crear la página. Intenta nuevamente."
    return handler_input.response_builder.speak(speech_text).response

@sb.request_handler(can_handle_func=lambda input: input.request_envelope.request.intent.name == "ConsultarPaginaIntent")
def consultar_pagina_handler(handler_input: HandlerInput):
    """
    Maneja la intención de consultar una página de Notion.
    Esta función se ejecuta cuando el usuario pregunta sobre una página específica en Notion, usando la <<frase adecuada>>.
    
    <<Frase adecuada>>: Se refiere a las palabras o expresiones que un usuario podría utilizar para activar la intención "ConsultarPaginaIntent". 
    Estas frases deben ser claras y específicas, permitiendo que Alexa reconozca y procese correctamente la solicitud del usuario. 

    Ejemplos:
    - "Consulta la página con ID [ID de la página]."
    - "¿Cuál es el título de la página [ID de la página]?"
    - "Dime qué dice la página [ID de la página]."
    - "Muéstrame la información de la página [ID de la página]."
    
    Responde (Alexa) al usuario con el título de la página solicitada.
    """
    try:
        # Obtenemos el ID de la página desde la solicitud
        pagina_id = handler_input.request_envelope.request.intent.slots["pagina_id"].value
        # URL para acceder a la API de Notion para la página en concreto
        url = f"https://api.notion.com/v1/pages/{pagina_id}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        page_data = response.json()

        # Txto de respuesta (lo que dirá Alexa), por ahora, con el título de la página
        speech_text = f"La página con ID {pagina_id} tiene el título: {page_data['properties']['title']['title'][0]['text']['content']}."
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            speech_text = f"No encontré la página con ID {pagina_id}. Verifica el número e intenta de nuevo."
        else:
            speech_text = "Hubo un problema al consultar la página. Por favor intenta nuevamente más tarde."
    except Exception:
        speech_text = "Ocurrió un error inesperado al consultar la página."
    return handler_input.response_builder.speak(speech_text).response

# La función para manejar la asignación de tareas debería en cuestión 
# verificar que los parámetros del discurso del usuario (quien asigna)
# sean los correctos para una tarea dada, es decir, delimitamos como se asignan las tareas
# e.g. "Alexa agrega la tarea <<tarea_1>> al <<usuario_1>> como fecha limite <<fecha_1>>"

@sb.global_request_handler(can_handle_func=lambda input: True)
def default_handler(handler_input: HandlerInput):
    """
    Manejador por defecto que se ejecuta si ninguna otra intención coincide.
    """
    return handler_input.response_builder.speak("No entendí tu solicitud. Por favor, intenta nuevamente.").response

if __name__ == "__main__":
    app.run(debug=True)

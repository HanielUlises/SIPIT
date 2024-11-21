from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import requests
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

model = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import requests
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Configuración constante
TOKEN_NOTION = "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"
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

ETIQUETAS = [{"name": "Web"}, {"name": "Mejora"}]
ESTADO = "En curso"
ID_PROYECTO = "1232595b-ac6f-816c-9240-dae9cbd7dfd8"


#Comandos de Notion

# Función principal para crear una nueva tarea en Notion
def CrearTarea(texto):
    # Definir el prompt para extraer valores del texto de entrada
    promptc = ChatPromptTemplate.from_template("""
    Extrae el nombre del proyecto, el nombre de la tarea, la fecha de inicio, la fecha de conclusión, el nivel de prioridad, el nombre
    de la persona a la que esta asignada, el estado y la descripción del siguiente comando:
    {texto}
    y que los valores tengan este formato: nombre_proyecto="valor",nombre_tarea="valor",nombre_persona="valor", estado="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor", resumen="valor".
    Devuelve estos datos como un diccionario JSON con las claves "nombre_proyecto","nombre_tarea","nombre_persona", "estado", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
    Unicamente devuelve el JSON. Sin comentarios ni explicación.
    """)

    # Extraer los datos necesarios con el modelo
    chainc = promptc | model | StrOutputParser()
    resultado_prompt = chainc.invoke({"texto": texto})
    datos_tarea = json.loads(resultado_prompt)
    print(datos_tarea)

    # Definir los datos de la nueva entrada combinando los parámetros extraídos y las constantes
    nueva_entrada = {
        "parent": {"database_id": ID_DATABASE},
        "properties": {
            "Nombre de la tarea": {
                "title": [{"text": {"content": datos_tarea["nombre_tarea"]}}]
            },
            "Titular": TITULAR,
            #"Estado": {
            #    "status": {"name": ESTADO}
            #},
              "Persona asignada": {
               "multi_select": [{"name": datos_tarea["nombre_persona"]}]
                                },
            "Estado": {
                "status": {"name": datos_tarea["estado"]}
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
            "Descripción": {
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
#texto = """SIPIT, crea una tarea con nombre "probando", que tenga fecha de inicio "01-11-2024" y con una fecha de conclusión "15-11-2024",
#con un nivel de prioridad "Alta", con la descripción "Revisar y ajustar los puntos críticos del proyecto", la persona asignada es Sam, y el estado es En curso."""
#CrearTarea(texto)


# Función principal para crear una nueva tarea en Notion
def CrearMinuta(texto):
    # Definir el prompt para extraer valores del texto de entrada
    promptc = ChatPromptTemplate.from_template("""
    Extrae el nombre de la minuta, la fecha de inicio, la fecha de conclusión, el nombre
    de los participantes y el resumen del siguiente comando:
    {texto}
    y que los valores tengan este formato: nombre_minuta="valor",participante="valor",objetiv="valor"  fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD",  resumen="valor".
    Devuelve estos datos como un diccionario JSON con las claves "objetivo","nombre_minuta","participante", "estado", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
    Unicamente devuelve el JSON. Sin comentarios ni explicación.
    """)

    # Extraer los datos necesarios con el modelo
    chainc = promptc | model | StrOutputParser()
    resultado_prompt = chainc.invoke({"texto": texto})
    datos_tarea = json.loads(resultado_prompt)
    print(datos_tarea)

    # Definir los datos de la nueva entrada combinando los parámetros extraídos y las constantes
    nueva_entrada = {
        "parent": {"database_id": ID_DATABASE},
        "properties": {
            "title": {
                "title": [{"text": {"content": datos_tarea["nombre_minuta"]}}]
            },
            #"Estado": {
            #    "status": {"name": ESTADO}
            #},
            "Participantes 1": {
               "multi_select": [{"name": datos_tarea["participante"]}]
                                },
            "Fecha": {
                "date": {
                    "start": datos_tarea["fecha_inicio"],
                    "end": datos_tarea["fecha_fin"]
                }
            },
            "Resumen": {
                "rich_text": [{"text": {"content": datos_tarea["resumen"]}}]
            },
            "Objetivo": {
                "rich_text": [{"text": {"content": datos_tarea["objetivo"]}}]
            }
        }
    }

    # Realizar la solicitud POST a la API de Notion para crear una nueva entrada
    respuesta = requests.post(URL_CREACION, headers=CABECERA, data=json.dumps(nueva_entrada))

    # Verificar si la solicitud fue exitosa y mostrar la respuesta
    if respuesta.status_code == 200:
        print("La minuta se creó con éxito en Notion.")
        #print(json.dumps(respuesta.json(), sort_keys=False, indent=4))
    else:
        print(f"Error {respuesta.status_code}: No se pudo crear la tarea.")
        print(json.dumps(respuesta.json(), sort_keys=False, indent=4))

# Ejemplo de uso
#texto = """SIPIT, crea una minuta con el nombre Prub, el objetivo es lala, los participantes presentes son Karina,
# realizada el "01-11-2024"  y resumen: no se hizo nada."""
#CrearMinuta(texto)


# Función principal para crear una nueva tarea en Notion
def CrearProyecto(texto):
    # Definir el prompt para extraer valores del texto de entrada
    promptc = ChatPromptTemplate.from_template("""
    Extrae el nombre del proyecto, la fecha de inicio, la fecha de conclusión, el estado, el nombre de la persona lider y el nivel de prioridad del siguiente comando:
    {texto}
    y que los valores tengan este formato: nombre="valor",estado="valor",lider="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor".
    Devuelve estos datos como un diccionario JSON con las claves "nombre","estado", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
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
                "status": {"name": datos_tarea["estado"]}
            },
            "Lider": {
               "multi_select": [{"name": datos_tarea["lider"]}]
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
#con un nivel de prioridad "Low", con el estado Atraso y el lider es Sam"."""
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
def ConsultarProyecto(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre del proyecto del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con las claves "NombreP", "fecha_inicio".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_consulta = json.loads(codigo)
    print(datos_consulta)

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "1232595bac6f81659e03db547d901cb9"

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
                    "property": "Nombre del proyecto",
                    "title": {
                        "equals": datos_consulta["NombreP"]
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
        interpreta: {text}. Dame un resumen de las propiedades de la tarea en español, dime el lider, las fechas , la prioridad y el estado.
        """
    )
    chain_interpretar = prompt_interpretar | model | StrOutputParser()
    interpretacion = chain_interpretar.invoke({"text": datos})

    return interpretacion

# Ejemplo de uso
texto = "SIPIT, resume el proyecto con nombre YUJU"

#resultado = ConsultarProyecto(texto)
#print(resultado)


# Función principal para consultar y procesar tareas
def ConsultarTareas(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre de la tarea del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con las claves "NombreT", "fecha_inicio".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_consulta = json.loads(codigo)

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "1232595bac6f81659e03db547d901cb9"

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
                    "property": "Nombre de la tarea",
                    "title": {
                        "equals": datos_consulta["NombreT"]
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
        interpreta: {text}. Dame un resumen de las propiedades de la tarea en español, dime aq uien esta asignada, las fechas y la prioridad.
        """
    )
    chain_interpretar = prompt_interpretar | model | StrOutputParser()
    interpretacion = chain_interpretar.invoke({"text": datos})

    return interpretacion

# Ejemplo de uso
texto = "SIPIT, resume la tarea con nombre Pruebita1"
#resultado = ConsultarTareas(texto)
#print(resultado)


# Función principal para consultar y procesar tareas
def ConsultarSprint(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre del Sprint del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con las claves "NombreS", "fecha_inicio".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_consulta = json.loads(codigo)

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "1232595bac6f8146a026d520ac1b0fed"

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
                    "property": "Nombre del Sprint",
                    "title": {
                        "equals": datos_consulta["NombreS"]
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
        interpreta: {text}. Dame un resumen de las propiedades del Sprint en español, dime el estado, las fechas y el procentaje d etareas completadas.
        """
    )
    chain_interpretar = prompt_interpretar | model | StrOutputParser()
    interpretacion = chain_interpretar.invoke({"text": datos})

    return interpretacion

# Ejemplo de uso
texto = "SIPIT, resume el Sprint con nombre Sprint 4"
#resultado = ConsultarSprint(texto)
#print(resultado)


# Función principal para consultar y procesar tareas
def ConsultarMinuta(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre del Sprint del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con las claves "NombreM", "fecha_inicio".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_consulta = json.loads(codigo)

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "13f2595bac6f80c1b9e1d5d80cc7bbbe"

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
                    "property": "title",
                    "title": {
                        "equals": datos_consulta["NombreM"]
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
        interpreta: {text}. Dame un resumen de las propiedades de la Minuta en español,
        dime las fecha, el objetivo, los participantes 1 y el resumen
        """
    )
    chain_interpretar = prompt_interpretar | model | StrOutputParser()
    interpretacion = chain_interpretar.invoke({"text": datos})

    return interpretacion

# Ejemplo de uso
texto = "SIPIT, consulta la minuta con nombre Prub"
#resultado = ConsultarMinuta(texto)
#print(resultado)


# Función para eliminar un proyecto
def EliminarProyecto(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre del proyecto del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con la clave "NombreP".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_proyecto = json.loads(codigo)
    print(datos_proyecto)

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "1232595bac6f81659e03db547d901cb9"

    # Paso 1: Obtener el ID del proyecto en Notion
    url_query = f"https://api.notion.com/v1/databases/{id_database}/query"
    cabecera = {
        "Authorization": f"Bearer {token_notion}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    filtro = {
        "filter": {
            "property": "Nombre del proyecto",
            "title": {
                "equals": datos_proyecto["NombreP"]
            }
        }
    }

    respuesta = requests.post(url_query, headers=cabecera, data=json.dumps(filtro))
    if respuesta.status_code != 200:
        print(f"Error {respuesta.status_code}: No se pudo obtener los datos del proyecto.")
        return None

    resultados = respuesta.json().get("results", [])
    if not resultados:
        print("No se encontró ningún proyecto con ese nombre.")
        return None

    proyecto_id = resultados[0]["id"]  # Toma el ID del primer resultado

    # Paso 2: Archivar (eliminar) el proyecto
    url_update = f"https://api.notion.com/v1/pages/{proyecto_id}"
    cuerpo = {
        "archived": True
    }

    respuesta_archivar = requests.patch(url_update, headers=cabecera, data=json.dumps(cuerpo))
    if respuesta_archivar.status_code == 200:
        print("Proyecto eliminado (archivado) con éxito.")
    else:
        print(f"Error {respuesta_archivar.status_code}: No se pudo archivar el proyecto.")

# Ejemplo de uso
texto = "elimina el proyecto con nombre: New Project"
#EliminarProyecto(texto)


# Función principal para eliminar una tarea
def EliminarTarea(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre de la tarea del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con la clave "NombreT".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_tarea = json.loads(codigo)
    print(datos_tarea)
    print(f"Tarea extraída: {datos_tarea}")

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "1232595bac6f812d8674d1f4e4012af9"

    # Paso 1: Obtener el ID de la tarea
    url_query = f"https://api.notion.com/v1/databases/{id_database}/query"
    cabecera = {
        "Authorization": f"Bearer {token_notion}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    filtro = {
        "filter": {
            "property": "Nombre de la tarea",
            "title": {
                "equals": datos_tarea["NombreT"]
            }
        }
    }

    respuesta = requests.post(url_query, headers=cabecera, data=json.dumps(filtro))
    if respuesta.status_code != 200:
        print(f"Error {respuesta.status_code}: No se pudo obtener los datos de la tarea.")
        return None

    resultados = respuesta.json().get("results", [])
    if not resultados:
        print("No se encontró ninguna tarea con ese nombre.")
        return None

    tarea_id = resultados[0]["id"]  # Toma el ID del primer resultado
    print(f"ID de la tarea encontrada: {tarea_id}")

    # Paso 2: Archivar (eliminar) la tarea
    url_update = f"https://api.notion.com/v1/pages/{tarea_id}"
    cuerpo = {
        "archived": True
    }

    respuesta_archivar = requests.patch(url_update, headers=cabecera, data=json.dumps(cuerpo))
    if respuesta_archivar.status_code == 200:
        print("Tarea eliminada (archivada) con éxito.")
    else:
        print(f"Error {respuesta_archivar.status_code}: No se pudo archivar la tarea.")

# Ejemplo de uso
texto = "elimina la tarea con nombre: FUNCION MAESTRA"
#EliminarTarea(texto)


# Función principal para eliminar un sprint
def EliminarSprint(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre del Sprint del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con la clave "NombreS".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_sprint = json.loads(codigo)
    print(f"Sprint extraído: {datos_sprint}")

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "1232595bac6f8146a026d520ac1b0fed"

    # Paso 1: Obtener el ID del sprint
    url_query = f"https://api.notion.com/v1/databases/{id_database}/query"
    cabecera = {
        "Authorization": f"Bearer {token_notion}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    filtro = {
        "filter": {
            "property": "Nombre del Sprint",
            "title": {
                "equals": datos_sprint["NombreS"]
            }
        }
    }

    respuesta = requests.post(url_query, headers=cabecera, data=json.dumps(filtro))
    if respuesta.status_code != 200:
        print(f"Error {respuesta.status_code}: No se pudo obtener los datos del sprint.")
        return None

    resultados = respuesta.json().get("results", [])
    if not resultados:
        print("No se encontró ningún sprint con ese nombre.")
        return None

    sprint_id = resultados[0]["id"]  # Toma el ID del primer resultado
    print(f"ID del sprint encontrado: {sprint_id}")

    # Paso 2: Archivar (eliminar) el sprint
    url_update = f"https://api.notion.com/v1/pages/{sprint_id}"
    cuerpo = {
        "archived": True
    }

    respuesta_archivar = requests.patch(url_update, headers=cabecera, data=json.dumps(cuerpo))
    if respuesta_archivar.status_code == 200:
        print("Sprint eliminado (archivado) con éxito.")
    else:
        print(f"Error {respuesta_archivar.status_code}: No se pudo archivar el sprint.")

# Ejemplo de uso
texto = "Elimina el Sprint con nombre Sprint 7"
#EliminarSprint(texto)


# Función principal para eliminar una minuta
def EliminarMinuta(texto):
    # Define el prompt para extraer valores del texto de entrada
    prompt_extract = ChatPromptTemplate.from_template(
        """
        Extrae el nombre de la minuta del comando:
        {texto}
        Devuelve estos datos como un diccionario JSON con la clave "NombreM".
        Unicamente devuelve el JSON. Sin comentarios ni explicación.
        """
    )

    # Genera código con valores extraídos
    valores_extraidos = prompt_extract | model | StrOutputParser()
    codigo = valores_extraidos.invoke({"texto": texto})
    datos_minuta = json.loads(codigo)
    print(f"Minuta extraída: {datos_minuta}")

    # Configuración para la consulta a la API de Notion
    token_notion = "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"
    id_database = "13f2595bac6f80c1b9e1d5d80cc7bbbe"

    # Paso 1: Obtener el ID de la minuta
    url_query = f"https://api.notion.com/v1/databases/{id_database}/query"
    cabecera = {
        "Authorization": f"Bearer {token_notion}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-02-22"
    }

    filtro = {
        "filter": {
            "property": "title",
            "title": {
                "equals": datos_minuta["NombreM"]
            }
        }
    }

    respuesta = requests.post(url_query, headers=cabecera, data=json.dumps(filtro))
    if respuesta.status_code != 200:
        print(f"Error {respuesta.status_code}: No se pudo obtener los datos de la minuta.")
        return None

    resultados = respuesta.json().get("results", [])
    if not resultados:
        print("No se encontró ninguna minuta con ese nombre.")
        return None

    minuta_id = resultados[0]["id"]  # Toma el ID del primer resultado
    print(f"ID de la minuta encontrada: {minuta_id}")

    # Paso 2: Archivar (eliminar) la minuta
    url_update = f"https://api.notion.com/v1/pages/{minuta_id}"
    cuerpo = {
        "archived": True
    }

    respuesta_archivar = requests.patch(url_update, headers=cabecera, data=json.dumps(cuerpo))
    if respuesta_archivar.status_code == 200:
        print("Minuta eliminada (archivada) con éxito.")
    else:
        print(f"Error {respuesta_archivar.status_code}: No se pudo archivar la minuta.")

# Ejemplo de uso
texto = "Elimina la minuta con nombre Prub"
#EliminarMinuta(texto)




#Actualizar

#Metodos necesarios

# Función para extraer el nombre de la tarea del texto
def ExtraerNombreTarea(texto):
    prompt = ChatPromptTemplate.from_template("""
    Extrae el nombre de la tarea del siguiente texto: {texto}.
    Devuelve solo el nombre de la tarea sin ningún comentario adicional.
    """)
    chain = prompt | model | StrOutputParser()
    nombre_tarea = chain.invoke({"texto": texto})
    return nombre_tarea.strip()

# Función para realizar búsqueda en la base de datos de Notion
def BuscarTarea(nombre_tarea):
    filtro = {
        "filter": {
            "property": "Nombre de la tarea",
            "rich_text": {
                "contains": nombre_tarea
            }
        }
    }

    # Realizar la solicitud a la API de Notion para buscar tareas
    respuesta = requests.post(URL_BUSQUEDA, headers=CABECERA, data=json.dumps(filtro))

    if respuesta.status_code == 200:
        tareas = respuesta.json().get("results", [])
        if tareas:
            print(f"Se encontraron {len(tareas)} tarea(s) con el nombre '{nombre_tarea}':")
            for tarea in tareas:
                nombre = tarea['properties']['Nombre de la tarea']['title'][0]['text']['content']
                print(f" - {nombre}")
        else:
            print(f"No se encontraron tareas con el nombre '{nombre_tarea}'.")
    else:
        print(f"Error {respuesta.status_code}: No se pudo realizar la búsqueda.")
        print(json.dumps(respuesta.json(), sort_keys=False, indent=4))

# Ejemplo de uso para buscar tarea
texto_busqueda = "Buscar tarea llamada 'Pruebita1'"
if 'buscar' in texto_busqueda.lower():
    nombre_tarea = ExtraerNombreTarea(texto_busqueda)
    BuscarTarea(nombre_tarea)

#Se terminan

# Función para extraer datos y actualizar la tarea en Notion
def ActualizarTarea(page_id, texto):
    promptc = ChatPromptTemplate.from_template("""
    Extrae el nombre del proyecto, el nombre de la tarea, la fecha de inicio, la fecha de conclusión, el nivel de prioridad, el nombre
    de la persona a la que esta asignada, el estado y la descripción del siguiente comando:
    {texto}
    y que los valores tengan este formato: nombre_proyecto="valor",nombre_tarea="valor",nombre_persona="valor", estado="valor", fecha_inicio="YYYY-MM-DD", fecha_fin="YYYY-MM-DD", prioridad="valor", resumen="valor".
    Devuelve estos datos como un diccionario JSON con las claves "nombre_proyecto","nombre_tarea","nombre_persona", "estado", "fecha_inicio", "fecha_fin", "prioridad" y "resumen".
    Unicamente devuelve el JSON. Sin comentarios ni explicación.
    """)

    # Extraer los datos necesarios con el modelo
    chainc = promptc | model | StrOutputParser()
    resultado_prompt = chainc.invoke({"texto": texto})
    print("Resultado del modelo:", resultado_prompt)  # Para ver cómo se ve el resultado del modelo

    # Limpiar la respuesta del modelo (eliminar saltos de línea y espacios extras)
    resultado_prompt_limpio = resultado_prompt.strip().replace("\n", "").replace(" ", "")

    # Intentamos cargar el JSON
    try:
        datos_tarea = json.loads(resultado_prompt_limpio)
        print("Datos extraídos:", datos_tarea)  # Ver los datos extraídos
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        return

    # Definir los datos de la actualización
    actualizacion_tarea = {
        "properties": {
            "Nombre de la tarea": {
                "title": [{"text": {"content": datos_tarea.get("nombre_tarea", "")}}]
            },
            "Persona asignada": {
                "multi_select": [{"name": datos_tarea.get("nombre_persona", "")}]
            },
            "Estado": {
                "status": {"name": datos_tarea.get("estado", "")}
            },
            "Fecha": {
                "date": {
                    "start": datos_tarea.get("fecha_inicio", ""),
                    "end": datos_tarea.get("fecha_fin", "")
                }
            },
            "Prioridad": {
                "select": {"name": datos_tarea.get("prioridad", "")}
            },
            "Descripción": {
                "rich_text": [{"text": {"content": datos_tarea.get("resumen", "")}}]
            }
        }
    }

    # Realizar la solicitud PATCH a la API de Notion para actualizar la tarea
    url_actualizacion = URL_ACTUALIZACION.format(page_id=page_id)
    respuesta = requests.patch(url_actualizacion, headers=CABECERA, data=json.dumps(actualizacion_tarea))

    # Verificar si la solicitud fue exitosa y mostrar la respuesta
    if respuesta.status_code == 200:
        print("La tarea se actualizó con éxito en Notion.")
    else:
        print(f"Error {respuesta.status_code}: No se pudo actualizar la tarea.")
        print(json.dumps(respuesta.json(), sort_keys=False, indent=4))

# Ejemplo de uso
#page_id = "1232595bac6f812d8674d1f4e4012af9"  # Aquí debes poner el ID de la página que quieres actualizar
#texto = """SIPIT, actualiza la tarea con nombre "Pruebita1", que tenga fecha de inicio "01-11-2024" y con una fecha de conclusión "15-11-2024",
#con un nivel de prioridad "Alta", con la descripción "Revisar y ajustar los puntos críticos del proyecto", la persona asignada es Sam, y el estado es Hecho."""
#ActualizarTarea(page_id, texto)

tokenNotion = "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"
idDataBase = "1232595bac6f81659e03db547d901cb9"  # Reemplaza con el ID de tu base de datos del calendario
urlCreacion = f"https://api.notion.com/v1/databases/{idDataBase}"

# Cabecera con autorización
cabecera = {
    "Authorization": f"Bearer {tokenNotion}",
    "Notion-Version": "2022-02-22"
}

# Realizar la solicitud GET a la API de Notion para obtener la base de datos
respuesta = requests.get(urlCreacion, headers=cabecera)

# Imprimir la respuesta en formato JSON
print(json.dumps(respuesta.json(), sort_keys=False, indent=4))



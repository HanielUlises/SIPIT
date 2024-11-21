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
    
class CrearMinutaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "CrearMinutaIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = CrearMinuta(texto)  # Llama a tu función ConsultarTareas
        speech_text = "La minuta ha sido creada." if resultado is None else f"Error al crear la minuta: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class CrearProyectoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "CrearProyectoIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = CrearProyecto(texto)  
        speech_text = "El proyecto ha sido creado." if resultado is None else f"Error al crear el proyecto: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class CrearSprintIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "CrearSprintIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = CrearSprint(texto)  # Llama a tu función ConsultarTareas
        speech_text = "El sprint ha sido creado." if resultado is None else f"Error al crear el sprint: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class CrearMinutaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "CrearMinutaIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = CrearMinuta(texto)  # Llama a tu función ConsultarTareas
        speech_text = "La minuta ha sido creada." if resultado is None else f"Error al crear la minuta: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
# Handler para consultar 
class ConsultarProyectoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "ConsultarProyectoIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = ConsultarProyecto(texto)  # Llama a tu función ConsultarTareas
        speech_text = f"El proyecto consultado: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response


class ConsultarTareasIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "ConsultarTareasIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = ConsultarTareas(texto)  # Llama a tu función ConsultarTareas
        speech_text = f"Las tareas consultadas son: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class ConsultarSprintIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "ConsultarSprintIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = ConsultarSprint(texto)  # Llama a tu función ConsultarTareas
        speech_text = f"El sprint consultado: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response

class ConsultarMinutaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "ConsultarMinutaIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = ConsultarMinuta(texto)  # Llama a tu función ConsultarMinuta
        speech_text = f"La minuta consultada: {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response

#Handlres para eliminar
    
class EliminarProyectoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "EliminarProyectoIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = EliminarProyecto(texto)  # Llama a tu función ConsultarTareas
        speech_text = "El proyecto ha sido eliminado" if resultado is None else f"Error al eliminar el proyecto {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class EliminarTareaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "EliminarTareaIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = EliminarTarea(texto)  
        speech_text = "La tarea ha sido eliminada" if resultado is None else f"Error al eliminar la tarea {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class EliminarSprintIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "EliminarSprintIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = EliminarSprint(texto)  
        speech_text = "El sprint ha sido eliminado" if resultado is None else f"Error al eliminar el sprint {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class EliminarMinutaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "EliminarMinutaIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = EliminarMinuta(texto)  
        speech_text = "La minuta ha sido eliminada" if resultado is None else f"Error al eliminar la minuta {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
    
class ActualizarTareaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # Reemplaza con tu lógica para determinar si debe manejar este intent
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "ActualizarTareaIntent"

    def handle(self, handler_input):
        texto = handler_input.request_envelope.request.intent.slots['texto'].value  # Obtén el texto del slot
        resultado = ActualizarTarea(texto)  
        speech_text = "La tarea ha sido eliminada" if resultado is None else f"Error al eliminar la tarea {resultado}"  # Modifica según tu lógica de respuesta
        return handler_input.response_builder.speak(speech_text).response
const Alexa = require('ask-sdk-core');
const AWS = require('aws-sdk'); // AWS SDK para manejar S3

// Configura el cliente de S3
const s3 = new AWS.S3();
const bucketName = 'sipit-transcriptions'; // Nombre de tu bucket de S3

// Lista para guardar las frases dictadas
let transcriptions = [];

// Manejador de la solicitud inicial
const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle(handlerInput) {
        const speakOutput = 'Hola, bienvenido a SIPIT. Di "Iniciar" seguido de lo que deseas dictar. Cuando termines, di "Genera la minuta".';
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    },
};

// Intent para transcribir lo que el usuario dicta
const TranscribeIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getIntentName(handlerInput.requestEnvelope) === 'TranscribeIntent';
    },
    handle(handlerInput) {
        const userInput = handlerInput.requestEnvelope.request.intent.slots.UserInput.value;

        // Agregar la frase a la lista de transcripciones
        transcriptions.push(userInput);

        const wordCount = transcriptions.join(' ').split(' ').length;
        const speakOutput = `He registrado tu frase. Hasta ahora tienes ${wordCount} palabras. ¿Algo más?`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt('¿Qué más deseas agregar?')
            .getResponse();
    },
};

// Intent para generar la minuta y subirla al bucket S3
const GenerateSummaryIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getIntentName(handlerInput.requestEnvelope) === 'GenerateSummaryIntent';
    },
    async handle(handlerInput) {
        if (transcriptions.length === 0) {
            const speakOutput = 'No has dictado nada. Por favor, di algo para transcribir.';
            return handlerInput.responseBuilder
                .speak(speakOutput)
                .getResponse();
        }

        // Consolidar transcripciones
        const fullText = transcriptions.join(' ');
        transcriptions = []; // Limpiar la lista para la próxima sesión

        // Nombre del archivo en el bucket
        const fileName = `transcription-${Date.now()}.txt`;

try {
    // Subir el archivo al bucket S3
    await s3
        .putObject({
            Bucket: bucketName,
            Key: fileName,
            Body: fullText,
            ContentType: 'text/plain',
        })
        .promise();

    const speakOutput = `El archivo con tu transcripción ha sido generado y guardado como ${fileName} en el bucket de S3.`;
    return handlerInput.responseBuilder
        .speak(speakOutput)
        .withSimpleCard('Resumen Generado', `Archivo: ${fileName}`)
        .getResponse();
} catch (error) {
    console.error('Error al subir a S3:', error);
    const speakOutput = `Hubo un problema al generar el archivo. Detalles del error: ${error.message}.`;
    return handlerInput.responseBuilder
        .speak(speakOutput)
        .getResponse();
}

    },
};

// Otros manejadores (Help, Cancel, Error)
const HelpIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        const speakOutput = 'Puedes dictar frases y luego generar una minuta que se guardará en S3.';
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt('¿Cómo puedo ayudarte?')
            .getResponse();
    },
};

const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.CancelIntent' ||
            Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.StopIntent';
    },
    handle(handlerInput) {
        const speakOutput = 'Adiós, hasta luego.';
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    },
};

const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.error('Error:', error);
        const speakOutput = 'Lo siento, hubo un problema. Intenta nuevamente.';
        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt('¿Podrías intentarlo nuevamente?')
            .getResponse();
    },
};

// Builder de la Skill
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        TranscribeIntentHandler,
        GenerateSummaryIntentHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler
    )
    .addErrorHandlers(ErrorHandler)
    .lambda();

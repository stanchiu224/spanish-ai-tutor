import gradio as gr
import openai
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {
        "role": "system",
        "content": """
    You are are a fun language tutor. In order to best help your students,
    you will ask them their age, target language level, and where they are from. You will
    reply to their questions using the target language as much as possible and clarify in English
    when necessary. If the student asks you a question in English, you will first reply with how
    they could ask the same question in the target language. 

    When asked about definitions of words or phrases, you will reply with the definition using 
    words and grammar the student likely understands given their language level. You will also provide examples of
    how to use the word or phrase that are funny and the student likely finds interesting given their age
    and cultural background.
    
    Limit all responses to 50 words or less.""",
    }
]


def transcribe_audio(audio_file) -> str:
    """Open and transcribe audio file using OpenAI's speech-to-text whisper API."""
    audio = open(audio_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio)
    return transcript["text"]


def gpt_response(text_question: str) -> str:
    """Ask a question and get a response from the tutor."""
    global messages

    messages.append({"role": "user", "content": text_question})

    response_json = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        frequency_penalty=1.0,
        presence_penalty=0.0,
    )

    # Return just the text of the response
    return response_json["choices"][0]["message"]["content"]


def chat_transcript(text_question: str, response_text: str) -> str:
    """Append the response to the chat transcript and create transcript."""

    global messages
    messages.append({"role": "assistant", "content": response_text})

    # Add the question and response to the chat transcript
    chat_transcript = ""
    for message in messages:
        if message["role"] != "system":
            chat_transcript += message["role"] + ": " + message["content"] + "\n\n"

    return chat_transcript


def audio_response(response_text: str):
    """Convert text response to audio using Azure's speech-to-text."""

    speech_key = os.getenv("SPEECH_KEY")
    service_region = os.getenv("SPEECH_REGION")

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "es-ES-IreneNeural"

    # use the selected speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(response_text).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(response_text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    return result


def audio_flow(audio_file: str) -> str:
    text_question = transcribe_audio(audio_file)
    AI_response = gpt_response(text_question)
    audio_response(AI_response)
    return chat_transcript(text_question, AI_response)


def text_flow(text_question: str) -> str:
    AI_response = gpt_response(text_question)
    audio_response(AI_response)
    return chat_transcript(text_question, AI_response)


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Hola! Digame su pregunta."""
    )
    with gr.Tab("Voz"):
        audio_file = gr.Audio(label="Pregunta", source="microphone", type="filepath")
        output = gr.Textbox(label="Respuesta")
        ask_button = gr.Button("Enviar")
        ask_button.click(fn=audio_flow, inputs=audio_file, outputs=output)

    with gr.Tab("Texto"):
        text_question = gr.Textbox(label="Pregunta")
        output = gr.Textbox(label="Respuesta")
        ask_button = gr.Button("Enviar")
        ask_button.click(fn=text_flow, inputs=text_question, outputs=output)

demo.launch()

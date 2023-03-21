# ChatGPT Language Tutor

## Description
This code provides a language tutoring chatbot that can be accessed through either voice or text input. The chatbot is powered by OpenAI's GPT-3.5 model, Whisper API, and Microsoft Azure's speecht-to-text API. The chatbot tutor is instructed to provide definitions and examples of usage in the target language. After receiving a user input, the chatbot responds with audio and then a transcript of the question and response are printed. The user can interact with the chatbot through a web interface provided by Gradio. The code includes functions for transcribing audio files, generating responses from GPT-3.5, creating chat transcripts, and converting text to speech.

A Poetry.lock file is included for required dependencies.

## Screenshot of the language tutor
![Screenshot of the chatbot](/images/screenshot-interface.png)

## Instructions

1. Get your OpenAI API key here - https://platform.openai.com/account/api-keys
2. Get a Microsoft Azure text-to-speech API key here - https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices
3. A Poetry.lock file is included for required dependencies. If you don't have Poetry for Python, install Poetry following the instructions here - https://python-poetry.org/docs/
4. Navigate to the directory where your poetry.lock file is located in your terminal.
5. Run the command `poetry install` to install all dependencies in the poetry.lock file.
6. Once the installation is complete, you should have a virtual environment set up. Activate the virtual environment using the following command: `poetry shell`
7. Create a ".env" file in the project's main directory. 
8. In the .env file, enter `OPENAI_API_KEY=xxxx` replacing the x's with your OpenAI API key.
9. In the .env file, repeat step 7 with `SPEECH_KEY=x` and `SPEECH_REGION=x` for your Azure text-to-speech API keys.
10. Run `python tutor.py` in your terminal and follow the gradio link to the language tutor chatbot interface.

## Disclaimer

This project is not affiliated with OpenAI in any way. Please read the OpenAI Terms of Service before using this project.

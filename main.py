import openai
'''In this code, OpenAI is used to generate AI-generated responses to user queries.
The `openai.Completion()` class is used to interact with the OpenAI API and generate responses
based on the given prompt/question. The generated response is then used in the conversation with the user.'''

import pyttsx3
'''Pyttsx3 is a text-to-speech conversion library used in this code. It provides a way to convert 
text into audible speech. The `pyttsx3.init()` function initializes the text-to-speech engine, 
and the `engine.say()` and `engine.runAndWait()` functions are used to speak the generated responses to the user.'''

import speech_recognition as sr
'''The SpeechRecognition library in this code enables the program to listen to and recognize 
speech input from the user. It uses the recognize_google() function to convert the captured
audio into text, allowing the program to understand and process the user's spoken commands.'''

import webbrowser 
'''The webbrowser module in this code allows the program to open web browsers and visit specified URLs.'''

from googletrans import Translator
'''The `googletrans` library in this code provides an interface to the Google Translate API. 
It is used to translate the generated AI responses from English to Marathi language using the
`Translator` class and the `translate()` function.'''
from apikey import api_data
'''It imports the variable "api_data" from the "apikey" file.'''

import sys
'''The line "import sys" in this code imports the sys module, which allows the program to interact 
with the Python interpreter and provides access to system-specific parameters and functions.'''

import googlemaps

# Set the OpenAI API key
openai.api_key = api_data

#we create an instance of the OpenAI completion class
completion = openai.Completion()

#here we create an instance of the pyttsx3 engine for text-to-speech conversion
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Create an instance of the Translator class
translator = Translator(service_urls=['translate.google.com'])

def generate_response(question):
    max_prompt_length = 4090
    max_completion_length = 4000

    if len(question) > max_prompt_length:
        question = question[0 :max_prompt_length]
        #if the question string exceeds its length it uses slicing to truncate the question

    prompt = f' User: {question}\n Jarvis: '
    """ The line creates a string `prompt` that combines the value of the `question` variable with fixed text "User: ", 
    a newline character `\n`, and " Jarvis: "."""
    
    max_tokens = max_completion_length - len(prompt)
    '''The line calculates the maximum number of tokens available for generating a response by subtracting the length of the
    `prompt` from the `max_completion_length`.'''
    
    response = completion.create(prompt=prompt, engine="text-davinci-002", stop=['\\User'], max_tokens=max_tokens)
    '''The line sends a completion request to the OpenAI API using the specified `prompt`, `engine`,
    `stop` sequence, and `max_tokens` parameters. It generates a response based on the given prompt using the specified language model.'''
    
    answer = response.choices[0].text.strip()
    #The .strip() method is used to remove any leading or trailing whitespace from the text. 
    return answer

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
    '''The `speak` function takes a `text` input and uses the text-to-speech engine (`engine`) to convert the text into audible speech.
    The `engine.say(text)` method is used to set the text to be spoken, and `engine.runAndWait()` is called to initiate the speech
    synthesis and wait for it to complete before continuing with the program execution.'''

def translate_text(text, target_language):
    translation = translator.translate(text, dest=target_language)
    return translation.text

'''The `translate_text` function takes a `text` input and a `target_language` parameter. It uses the `translator`
object to translate the `text` to the specified `target_language`. The translated text is then returned as the 
 output of the function.'''

# Set the encoding to UTF-8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

speak("Hello friend, how can I help you?")

def take_command():
    r = sr.Recognizer()
    #it takes command from the user and this function recognite the input of the user

    with sr.Microphone() as source:
        print('Listening...!!')
        r.pause_threshold = 1
        audio = r.listen(source)
        '''These lines set up the microphone as the audio source, print a message indicating that the program is
        listening, and use the SpeechRecognition library to listen and capture the audio input from the microphone
        as an `audio` object.'''

    try:
        query = r.recognize_google(audio, language='en-in')
        print("User Said: {} \n".format(query))
        return query
    except Exception as e:
        print("Say That Again...")
        return None
    
    '''In this code, the captured audio is passed to the `recognize_google` function from the SpeechRecognition
    library to convert it into text. If the audio is successfully recognized, the recognized text is printed as
    "User Said: " followed by the text, and then returned as the `query`. If an exception occurs during the recognition
    process, the program prints "Say That Again..." and returns `None`.'''

if __name__ == '__main__':
    while True:
        query = take_command()

        if query is None:
            continue

        print(query)

        if 'goodbye' in query.lower():
            print("Jarvis: Goodbye friend! \nHave a nice day")
            speak("Goodbye friend! Have a nice day")
            break
        
        """if 'Thank you' in query.lower():
            print("Jarvis: Do you need any kind of information?")
            speak("Do you need any kind of information?")
            break"""

        if 'open youtube' in query:
            webbrowser.open("www.youtube.com")

        if 'open google' in query:
            webbrowser.open("www.google.com")

        if 'bye' in query:
            break

        response = generate_response(query)
        translated_response = translate_text(response, 'mr')
        print("Jarvis in Marathi: {}".format(translated_response))
        print("Jarvis in English: {}".format(response))
        
        speak(response)  
        # Speak the translated response 

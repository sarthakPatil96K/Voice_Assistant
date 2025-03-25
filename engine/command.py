import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 175)
    engine.setProperty('voice', voices[1].id)
    eel.DisplayMessage(f"{text}")
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()
    eel.ShowHood()


@eel.expose
def TakeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source,10,6)
    try :
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said:{query}")
        eel.DisplayMessage(f"User said:{query}")
    except Exception as e:
        print("Sorry,I did not catch that")
        return ""
    return query.lower()
# text=TakeCommand()
# if text:
#     spaek(text)
@eel.expose
def allCommands(message=None):
    try:
        if message is None:
            query = TakeCommand()
            eel.senderText(query)
        else:
            query = message
            eel.senderText(message)


        if "open" in query:
            from engine.features import openCommand
            eel.spawn(openCommand, query)  # Runs in a separate thread
        elif "play" in query and "youtube" in query:
            from engine.features import PlayYoutube
            eel.spawn(PlayYoutube, query)
        elif "search" in query and "wikipedia" in query:
            from engine.features import search_wikipedia
            eel.spawn(search_wikipedia, query)
        elif "search" in query:
            from engine.features import search_google
            eel.spawn(search_google, query)
        elif "temperature" in query:
            from engine.features import weather
            eel.spawn(weather, query)
        elif "news" in query:
            from engine.features import news
            eel.spawn(news)
        elif "meaning" in query:
            from engine.features import dictionary_search
            eel.spawn(dictionary_search, query)
        elif "send message" in query or "phone call" in query or "video call" in query:
                from engine.features import findContact, whatsApp
                contact_no, name = findContact(query)
                if(contact_no == 0):
                    speak("Contact does not exist please add the contact number first!")
                else:
                
                    if "send message" in query and contact_no !=0:
                        message = 'message'
                        speak("what message to send")
                        query = TakeCommand()
                                                
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                                
                    whatsApp(contact_no, query, message, name)
        elif "add" in query:
            from engine.db import add_contact_from_query
            add_contact_from_query(query)
        elif "close" in query or "application" in query:
            from engine.features import close_app, extract_app_name
            app = extract_app_name(query)
            if app != None:
                close_app(app)
        elif "shutdown" in query or "exit" in query:
            from engine.features import close_voice_assistant
            close_voice_assistant()
        elif "alarm" in query or "set" in query or "reminder" in query:
            from engine.features import set_alarm,extract_time_and_message
            t,msg = extract_time_and_message(query)
            if query is not None:
                set_alarm(t,msg)
            else:
                speak("Error occured")
        else:
            from engine.features import chatBot
            eel.spawn(chatBot, query)
    except:
        print("Error")
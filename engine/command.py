import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 175)
    engine.setProperty('voice', voices[1].id)
    eel.DisplayMessage(f"User said:{text}")
    engine.say(text)
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
def allCommands():
    query = TakeCommand()

    if "open" in query:
        from engine.features import openCommand
        openCommand(query)
    elif "play" in query and "youtube" in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    elif "search" in query and "wikipedia" in query:
        from engine.features import search_wikipedia
        search_wikipedia(query)
    elif "search" in query:
        from engine.features import search_google
        search_google(query)
    elif "temperature" in query:
        from engine.features import weather
        weather(query)
    elif "news" in query:
        from engine.features import news
        news()
    else:
        from engine.features import chatBot
        response= chatBot(query)
        

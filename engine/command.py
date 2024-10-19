import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 175)
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def TakeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source,10,6)
    try :
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said:{query}")
    except Exception as e:
        print("Sorry,I did not catch that")
        return ""
    return query.lower()
# text=TakeCommand()
# if text:
#     spaek(text)

def allCommands():
    query = TakeCommand()

    if "open" in query:
        from engine.features import openCommand
        openCommand(query)
    elif "play" in query and "youtube" in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)
    else:
        print("not run")

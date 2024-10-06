import os
from playsound import playsound
from engine.config import Assistant_Name
from engine.command import speak

# voice assistant opening sound function
def playAssitantSound():
    music_dir="www\\assets\\audio\mixkit-software-interface-back-2575.wav"
    playsound(music_dir)

def openCommand(query):
    query=query.replace(Assistant_Name,"")
    query=query.replace("open","")
    query.lower()
    print("Openning "+query)

    if query!="":
        speak("Openning "+query)
        os.system("start "+query)
    else:
        speak("Not found")
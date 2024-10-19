import os
import re
from playsound import playsound
from engine.config import Assistant_Name
from engine.command import speak

import pywhatkit as kit

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
            query=query.replace("powerpoint","powerpnt")
            query=query.replace("whatsapp","whatsapp:")
            query=query.replace("word","winword")
            os.system("start "+query)
        
    else:
        speak("Not found")

def PlayYoutube(query):
    search_term=extract_yt_term(query)
    speak("playing"+search_term+"on youtube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None


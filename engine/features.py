import os
import re
import wikipedia as wk
import webbrowser
from playsound import playsound
from engine.config import Assistant_Name
from engine.command import speak
import eel
import pywhatkit as kit

import sqlite3
conn = sqlite3.connect("Eleven.db")
cursor = conn.cursor()

# voice assistant opening sound function
@eel.expose
def playAssitantSound():
    music_dir="www\\assets\\audio\mixkit-software-interface-back-2575.wav"
    playsound(music_dir)

def openCommand(query):
    query=query.replace(Assistant_Name,"")
    query=query.replace("open","")
    query.lower()
    print("Openning "+query)
    app_name = query.strip()

    if app_name !='':
        try:
            cursor.execute(
                'SELECT path FROM sys_commands WHERE name IN (?)',(app_name,)
            )
            results = cursor.fetchall()

            if len(results) !=0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    'SELECT url FROM web_commands WHERE name IN (?)',(app_name,)
                )
                results = cursor.fetchall()

                if len(results) !=0:
                    speak("Opening "+ query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Openning "+query)

                    try:
                        query=query.replace("powerpoint","powerpnt")
                        query=query.replace("whatsapp","whatsapp:")
                        query=query.replace("word","winword")
                        os.system("start "+query)

                    except:
                        speak("Not found")

        except:
            speak("Something went wrong")



     

def PlayYoutube(query):
    search_term=extract_yt_term(query)
    speak("playing"+search_term+"on youtube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
     
    match = re.search(pattern, command, re.IGNORECASE)
     
    return match.group(1) if match else None

def search_wikipedia(query):
    try:
        search_term = extract_wk_term(query)
        print(f"Searching Wikipedia for: {search_term}")
        result = wk.summary(search_term, sentences=3)  # Fetches the first 3 sentences of the search result
        print(result)   
        speak(result)   
    except Exception as e:
        speak(f"An error occurred: {e}")

def extract_wk_term(command):
     
    pattern = r'search\s+(.*?)\s+on\s+wikipedia'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

 
def search_google(query):
    search_term = extract_google_term(query)
    print(f"Searching Google for: {search_term}")
    speak(f"Searching Google for {search_term}")
    kit.search(search_term)  # This will open the search in a browser

def extract_google_term(command):
    # Extract search term from command using regex
    pattern = r'search\s+(.*?)\s+on\s+google'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None

 

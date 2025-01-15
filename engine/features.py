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
from hugchat import hugchat
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

 
# chatBot using open source library
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.jason")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# weather API
def weather(query):
    text = extract_city_from_query(query)
    import requests,json
    api_key = "e18c82c4cf1a4f6864b3bf11bd6e6121"
    url = "https://api.openweathermap.org/data/2.5/weather?q="
    cmpl_url = url + text+ "&appid=" +api_key
    response = requests.get(cmpl_url)
    response = response.json()
    understandable_lang = format_weather_data(response)
    speak(understandable_lang)
    return response

# extract city name
def extract_city_from_query(query):
     
    # Common pattern for city names (basic implementation)
    # Adjust this to match your requirements or use a predefined list of cities for better accuracy.
    pattern = r"temperature in ([A-Za-z\s]+)"
    
    match = re.search(pattern, query, re.IGNORECASE)
    if match:
        # Return the city name, stripping any extra whitespace
        return match.group(1).strip()
    return None

def format_weather_data(api_response):
     
    # Extract required fields from the response
    temperature_kelvin = api_response.get("main", {}).get("temp")
    pressure = api_response.get("main", {}).get("pressure")
    humidity = api_response.get("main", {}).get("humidity")
    temp_min_kelvin = api_response.get("main", {}).get("temp_min")
    temp_max_kelvin = api_response.get("main", {}).get("temp_max")

    # Convert temperatures from Kelvin to Celsius
    temperature_celsius = temperature_kelvin - 273.15 if temperature_kelvin else None
    temp_min_celsius = temp_min_kelvin - 273.15 if temp_min_kelvin else None
    temp_max_celsius = temp_max_kelvin - 273.15 if temp_max_kelvin else None

    # Format the output
    output = []
    if temperature_celsius is not None:
        output.append(f"Current Temperature: {temperature_celsius:.2f}°C ")
    if temp_min_celsius is not None and temp_max_celsius is not None:
        output.append(f"Temperature Range: {temp_min_celsius:.2f}°C to {temp_max_celsius:.2f}°C ")
    if pressure is not None:
        output.append(f"Pressure: {pressure} hPa ")
    if humidity is not None:
        output.append(f"Humidity: {humidity}%")

    return "\n".join(output) if output else "Weather data not available."

# News API

def news():
    import requests
    url = "http://api.mediastack.com/v1/news?access_key=a40867165592e001d48e80ed52bc9ec1&countries=in"
    response = requests.get(url)
    response = response.json()
    speak_response = format_news_for_voice_assistant(response["data"][0])
    speak(speak_response)
    return speak_response

  
def format_news_for_voice_assistant(news_json):
    # Extracting the relevant information from the news API response
    title = news_json.get("title", "No title available")
    description = news_json.get("description", "No description available")
    source = news_json.get("source", "Unknown source")
    published_at = news_json.get("published_at", "No publish date available")
    url = news_json.get("url", "No URL available")

    # Formatting the information for voice assistant
    speakable_text = f"Here's a news update: {title}. {description}  Source: {source}."
    
    return speakable_text

 
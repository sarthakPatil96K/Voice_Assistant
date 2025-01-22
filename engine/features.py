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
    """
    Searches for a term on Google based on the user's query.
    
    Args:
        query (str): The user's input query.
    """
    search_term = extract_google_term(query)
    
    if search_term:
        print(f"Searching Google for: {search_term}")
        speak(f"Searching Google for {search_term}")
        kit.search(search_term)  # This will open the search in a browser
    else:
        speak("I couldn't determine what to search for. Please try again with a clearer query.")


def extract_google_term(command):
    """
    Extracts the search term from a user's query to search on Google.
    
    Args:
        command (str): The user's input query.
    
    Returns:
        str: The extracted search term or None if no term is found.
    """
    # Convert command to lowercase for consistent matching
    command = command.lower()
    
    # Define patterns for common search queries
    patterns = [
        r"search\s+(.*?)\s+on\s+google",  # Example: "Search Python on Google"
        r"google\s+(.*)",                # Example: "Google Python"
        r"search\s+(.*)",                # Example: "Search Python"
        r"look up\s+(.*?)\s+on\s+google" # Example: "Look up Python on Google"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            return match.group(1)  # Return the captured search term
    
    # Fallback: Extract remaining words after "search", "google", or "look up"
    fallback_pattern = r"(?:search|google|look up)\s+(.*)"
    fallback_match = re.search(fallback_pattern, command)
    return fallback_match.group(1) if fallback_match else None

 
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

def dictionay_search(query):
    """
    Searches for a word in the dictionary API and speaks the response.
    
    Args:
        query (str): The user's input query.
    """
    import requests

    # Extract the word to search
    word = extract_word_from_query(query)
    
    if not word:
        speak("I couldn't extract a word to search. Please try rephrasing your query.")
        return
    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        response_data = response.json()
        refined_response = process_dictionary_response_refined(response_data)
        speak(refined_response)
    else:
        speak(f"Error: Unable to fetch data for the word '{word}'. Status code: {response.status_code}")


def extract_word_from_query(query):
    """
    Extracts a word to search in the dictionary from a user's query.
    
    Args:
        query (str): The user's input query.
    
    Returns:
        str: The extracted word or None if no word is found.
    """
    import re

    # Convert query to lowercase
    query = query.lower()
    
    # Patterns for extracting the word
    patterns = [
        r"what does (\w+) mean",           # Example: "What does apple mean?"
        r"meaning of (\w+)",               # Example: "Meaning of apple"
        r"definition of (\w+)",            # Example: "Definition of apple"
        r"what is the definition of (\w+)" # Example: "What is the definition of apple?"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(1)  # Return the captured word
    
    # Fallback: Extract the last word in the query
    words = re.findall(r"\b[a-zA-Z]+\b", query)  # Match only valid words
    return words[-1] if words else None

def process_dictionary_response_refined(data, word_limit=100):
    """
    Converts dictionary API response into a concise, speakable language format, ignoring unwanted characters.
    
    Args:
        data (list): Parsed JSON response from the dictionary API.
        word_limit (int): Maximum word count for the output.
    
    Returns:
        str: A refined, concise, and speakable version of the dictionary entry.
    """
    try:
        if not data or not isinstance(data, list):
            return "The dictionary response is empty or invalid."
        
        # Extract the first entry
        entry = data[0]
        word = entry.get("word", "Unknown word")
        phonetic = entry.get("phonetic", "No phonetic available")
        phonetic = re.sub(r"[^a-zA-Z\s]", "", phonetic)  # Remove unwanted characters from phonetic
        meanings = entry.get("meanings", [])
        
        # Create the speakable response
        response = [f"The word is '{word}'. It is pronounced as '{phonetic}'."]
        word_count = sum(len(sentence.split()) for sentence in response)

        for meaning in meanings:
            if word_count >= word_limit:
                break
            part_of_speech = meaning.get("partOfSpeech", "unknown")
            definitions = meaning.get("definitions", [])
            
            for definition in definitions:
                if word_count >= word_limit:
                    break
                definition_text = definition.get("definition", "No definition provided.")
                example = definition.get("example", None)
                
                # Clean definition and example of unwanted characters
                definition_text = re.sub(r"[^a-zA-Z0-9\s.,']", "", definition_text)
                if example:
                    example = re.sub(r"[^a-zA-Z0-9\s.,']", "", example)

                response.append(f"As a {part_of_speech}, it means: {definition_text}.")
                word_count += len(response[-1].split())
                
                if example and word_count < word_limit:
                    response.append(f"For example: {example}.")
                    word_count += len(response[-1].split())

        # Combine and truncate if necessary
        final_response = " ".join(response)
        if len(final_response.split()) > word_limit:
            final_response = " ".join(final_response.split()[:word_limit]) + "..."
        
        return final_response
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

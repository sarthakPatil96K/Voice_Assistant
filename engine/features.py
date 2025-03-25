import os
import re
from shlex import quote
import struct
import subprocess
import sys
import pvporcupine
import pyaudio
import pyautogui
import wikipedia as wk
import webbrowser
from playsound import playsound
from engine.config import Assistant_Name
from engine.command import speak
import eel
import pywhatkit as kit
import time
import sqlite3
import psutil
from hugchat import hugchat
conn = sqlite3.connect("Eleven.db")
cursor = conn.cursor()

# voice assistant opening sound function
@eel.expose
def playAssitantSound():
    print("sound played")
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
        print(f"Searching on Google for: {search_term}")
        speak(f"Searching on Google for {search_term}")
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

import time
from hugchat import hugchat
from hugchat.exceptions import ChatError

 
def sanitize_response(response):
    """Ensures the response is a string and removes unwanted characters."""
    if not isinstance(response, str):
        response = str(response)  # Convert response to a string if it's not
    return re.sub(r"[*\\/]", "", response)  # Remove *, \, /

def chatBot(query):
    try:
        user_input = query.lower()
        chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
        
        # Start a new conversation and set it
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)
        
        # Send the query to the chatbot
        response = chatbot.chat(user_input)
        
        # Introduce a delay to respect rate limits
        time.sleep(2)
        
        # Sanitize the response before speaking
        cleaned_response = sanitize_response(response)
        
        # Print and speak the sanitized response
        print(cleaned_response)
        speak(cleaned_response)
        return cleaned_response

    except ChatError as e:
        print(f"ChatError: {e}")
        response = "I'm experiencing some issues. Please try again later."
        speak(response)
        return response

    except FileNotFoundError:
        print("Cookie file not found. Ensure the path is correct.")
        response = "Configuration error. Please check the setup."
        speak(response)
        return response

    except Exception as e:
        print(f"Unexpected error: {e}")
        response = "An unexpected error occurred. Please try again."
        speak(response)
        return response


# weather API
def weather(query):
    import requests

    api_key = "e18c82c4cf1a4f6864b3bf11bd6e6121"  # Replace with your valid API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="

    try:
        # Extract city name from query
        city = query.replace("temperature in", "").strip()

        if not city:
            speak("Please specify a city for the weather.")
            return

        # Construct API URL
        cmpl_url = base_url + city + "&appid=" + api_key + "&units=metric"

        # Make the API call
        response = requests.get(cmpl_url)
        if response.status_code != 200:
            speak("Unable to fetch weather data. Please try again.")
            print(f"Weather API Error: {response.status_code}, {response.text}")
            return

        # Parse the response
        weather_data = response.json()
        if "main" in weather_data:
            temp = weather_data["main"]["temp"]
            condition = weather_data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {condition}.")
        else:
            speak("Could not find weather details for the specified city.")
    except Exception as e:
        speak(f"An error occurred while fetching weather data: {str(e)}")
        print(f"Weather Function Exception: {str(e)}")


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

def dictionary_search(query=None):
    import requests
    word = extract_word_for_dictionary(query)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        response_data = response.json()
        response = concise_dictionary_response(response_data)
        speak(response)
        return  response
    else:
        print(f"Error: Unable to fetch data for the word '{word}'. Status code: {response.status_code}")

def extract_word_for_dictionary(query):
    """
    Extracts the word to search in a dictionary from the user's query.

    Args:
        query (str): The user's input query.

    Returns:
        str: The extracted word or None if no word is found.
    """
    # Common patterns for dictionary queries
    patterns = [
        r"meaning of (\w+)",         # Example: "meaning of hero"
        r"what does (\w+) mean",     # Example: "what does hero mean"
        r"define (\w+)",             # Example: "define hero"
        r"definition of (\w+)",      # Example: "definition of hero"
        r"what is (\w+)",            # Example: "what is hero"
        r"meaning (\w+)"             # Example: "meaning hero"
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1)  # Return the matched word

    # If no pattern matches, return None
    return None


def concise_dictionary_response(data, word_limit=50):
    """
    Converts dictionary API response into a concise, speakable language format.
    
    Args:
        data (list): Parsed JSON response from the dictionary API.
        word_limit (int): Maximum word count for the output.
    
    Returns:
        str: A concise and speakable version of the dictionary entry.
    """
    try:
        if not data or not isinstance(data, list):
            return "The dictionary response is empty or invalid."
        
        # Extract the first entry
        entry = data[0]
        word = entry.get("word", "Unknown word")
        phonetic = entry.get("phonetic", "No phonetic available")
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
    
def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string


# find contacts
def findContact(query):
    
    words_to_remove = ['make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

import pyautogui
import subprocess
import time
import threading
import urllib.parse  # For URL encoding

def speak_async(message):
    threading.Thread(target=speak, args=(message,)).start()

def whatsApp(mobile_no, message, flag, name):
    try:
        if flag == 'message':
            # URL encode the message to handle special characters
            encoded_message = urllib.parse.quote(message)
            
            # Use the WhatsApp desktop app URL scheme with the encoded message
            whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
            
            # Open WhatsApp Desktop
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
            time.sleep(10)  # Increased wait time to ensure WhatsApp is fully loaded
            pyautogui.hotkey('enter')
            jarvis_message = f"Message sent successfully to {name}"

        else:  # For voice and video calls
            whatsapp_url = f"whatsapp://send?phone={mobile_no}"
            
            # Launch WhatsApp Desktop App
            subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
            time.sleep(7)

            # Maximize window
            pyautogui.hotkey('win', 'up')
            time.sleep(1)

            if flag == 'call':
                jarvis_message = f"Calling {name}"

                # Locate call button or use fallback navigation
                call_button = pyautogui.locateOnScreen(r"www/assets/IMG/voice_call.png", confidence=0.8)

                if call_button:
                    pyautogui.click(call_button)
                else:
                    print("Voice call button not found, using tab navigation.")
                    
                    for _ in range(5):   # Adjusted tab count
                        pyautogui.hotkey('tab')
                        time.sleep(0.3)

                    pyautogui.hotkey('enter')

            elif flag == 'video':
                jarvis_message = f"Starting video call with {name}"
                video_button = pyautogui.locateOnScreen(r"www/assets/IMG/video_call.png", confidence=0.8)

                if video_button:
                    pyautogui.click(video_button)
                else:
                    print("Video call button not found, using tab navigation.")
                    
                    for _ in range(4):   # Adjusted tab count
                        pyautogui.hotkey('tab')
                        time.sleep(0.3)

                    pyautogui.hotkey('enter')

        # Speak confirmation message
        speak_async(jarvis_message)

    except Exception as e:
        print(f"Error: {e}")
        speak_async("There was an issue with the WhatsApp operation.")



@eel.expose
def close_voice_assistant():
    """Closes the Eel frontend and exits Python."""
    farewell_message = "Goodbye! Shutting down the assistant."
    print(farewell_message)
    speak(farewell_message)

    # Call JavaScript function to close the frontend
    eel.closeWindow()  

    # Exit the Python backend after a short delay
    sys.exit()

# function to close application
import psutil
import os
import eel

def close_app(app_name):
    app_name = app_name.lower()  # Make the app name case-insensitive
    closed_apps = []

    # Iterate through all running processes to find WhatsApp or related app
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if app_name in process.info['name'].lower():  # Check if app name matches
                print(f"Found {process.info['name']} (PID: {process.info['pid']})")
                process.kill()  # Kill the process
                closed_apps.append(process.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Provide feedback to the user on whether any apps were closed
    if closed_apps:
        message = f"Closed the app {app_name}."
        speak(message)
        return message
    else:
        message = f"No running instances of {app_name} found."
        speak(message)
        return message


def extract_app_name(command):
    """
    Extracts the application name from the voice command.
    
    Example voice commands:
    - "close chrome"
    - "open notepad"
    
    Returns:
    - The extracted application name (e.g., 'chrome', 'notepad')
    """
    # List of common keywords (close, open, etc.)
    action_keywords = ['close', 'open', 'launch', 'start', 'kill', 'stop']
    
    # Remove the action keyword from the command
    command = command.lower()
    for keyword in action_keywords:
        if keyword in command:
            command = command.replace(keyword, '').strip()
            break

    # We can also handle edge cases, such as if there is more than one word.
    # Clean the string by removing extra spaces and handling the app name
    app_name = command.strip()
    
    # Optionally, validate app name (if needed)
    # You can use a regex or predefined app list to match common app names
    app_name = re.sub(r'[^a-zA-Z0-9\s]', '', app_name)  # Remove non-alphanumeric characters
    
    return app_name

 
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# setting alarm
import datetime
import threading
import os
import platform
import time

def play_alarm():
    """Plays the alarm sound based on the OS."""
    print("⏰ Alarm ringing!")
    
    if platform.system() == "Windows":
        os.system("start ms-winsoundevent:Notification.Default")
    elif platform.system() == "Darwin":  # macOS
        os.system("say 'Alarm ringing!'")
    else:  # Linux
        os.system("paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga")

def play_alarm():
    """Plays an alarm sound."""
    try:
        # Use a built-in sound file or specify your own
        sound_file = "www\\assets\\audio\\alarm_sound.mp3"  # Replace with a valid sound file
        playsound(sound_file)
    except Exception as e:
        print(f"Error playing sound: {e}")

def set_alarm(alarm_time, message="Alarm ringing!"):
    """
    Sets an alarm at the specified time in a separate thread.
    
    Parameters:
    - alarm_time (str): Time in HH:MM format (24-hour).
    - message (str): Message to display when the alarm rings.
    """
    def alarm_thread():
        try:
            alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
            now = datetime.datetime.now()
            alarm_datetime = now.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

            # Handle next-day alarm
            if alarm_datetime < now:
                alarm_datetime += datetime.timedelta(days=1)

            # Sleep until the alarm time
            while datetime.datetime.now() < alarm_datetime:
                time.sleep(1)

            # Trigger the alarm
            print(message)
            speak(message)
            play_alarm()

        except Exception as e:
            print(f"Error: {e}")

    # Start the alarm in a separate thread
    speak("Your alarm has been set!!")
    threading.Thread(target=alarm_thread).start()
    print(f"✅ Alarm set for {alarm_time}. Running in background...")


import re

def extract_time_and_message(query):
    """
    Extracts time and generates a contextual message from the user's query,
    removing redundant words.
    
    Parameters:
    - query (str): User's voice query
    
    Returns:
    - tuple: (time in HH:MM format, contextual message) or (None, query) if no time is found
    """
    
    # Remove redundant words
    redundant_words = [
        "set an alarm at", "set alarm at", "set reminder at", "remind me", 
        "wake me up", "notify me", "alert me"
    ]
    
    # Clean up the query
    for word in redundant_words:
        query = re.sub(rf'\b{word}\b', '', query, flags=re.IGNORECASE).strip()

    # Regex patterns for time formats
    patterns = [
        r'(\d{1,2}):(\d{2})\s?(AM|PM|am|pm)?',         # 12-hour with AM/PM
        r'(\d{1,2})\s?(AM|PM|am|pm)',                   # 12-hour without minutes
        r'(\d{1,2}):(\d{2})'                            # 24-hour format
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            # Extract time components
            if len(match.groups()) == 3:  # 12-hour with AM/PM
                hour, minute, meridian = match.groups()
                hour, minute = int(hour), int(minute)

                if meridian:
                    if meridian.lower() == "pm" and hour != 12:
                        hour += 12
                    elif meridian.lower() == "am" and hour == 12:
                        hour = 0
            elif len(match.groups()) == 2 and ":" not in match.group(0):  # 12-hour without minutes
                hour, meridian = match.groups()
                hour = int(hour)
                minute = 0
                if meridian.lower() == "pm" and hour != 12:
                    hour += 12
                elif meridian.lower() == "am" and hour == 12:
                    hour = 0
            else:  # 24-hour format
                hour, minute = map(int, match.groups()[:2])

            # Format the time in HH:MM
            time_str = f"{hour:02d}:{minute:02d}"

            # Extract the message by removing the time from the query
            message = re.sub(pattern, '', query).strip()

            # Generate contextual message
            if message:
                if any(word in message.lower() for word in ["meeting", "event", "appointment","lecture"]):
                    contextual_msg = f"Time {message}"
                elif any(word in message.lower() for word in ["call", "remind", "notify"]):
                    contextual_msg = f"Reminding you to {message}"
                else:
                    contextual_msg = message
            else:
                contextual_msg = "Alarm ringing!"

            return time_str, contextual_msg

    # If no time is found, return the full query as the message
    return None, query

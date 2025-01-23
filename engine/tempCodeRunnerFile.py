
def dictionay_search():
    import requests
    word = "Hero" 
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    if response.status_code == 200:
        response_data = response.json()
        print(concise_dictionary_response(response_data))

    else:
        print(f"Error: Unable to fetch data for the word '{word}'. Status code: {response.status_code}")
 

def concise_dictionary_response(data, word_limit=100):
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

# Call the function
dictionay_search()
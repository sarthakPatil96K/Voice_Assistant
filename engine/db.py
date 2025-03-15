import re
import sqlite3
from engine.command import speak
 
conn = sqlite3.connect("Eleven.db")
cursor = conn.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_commands(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
# cursor.execute(query)

# # query = "UPDATE sys_commands set name =? WHERE id = ?"
# # data =("ms edge",6)
# # cursor.execute(query,data)
# # conn.commit()

# query = "CREATE TABLE IF NOT EXISTS web_commands(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)


# # query = "INSERT INTO web_commands VALUES(null,'rgit college','https://www.mctrgit.ac.in/')"
# # cursor.execute(query)
# # conn.commit()
# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# query = "INSERT INTO contacts VALUES (null,'paras', '8652305374', 'null')"
# cursor.execute(query)
# conn.commit()
def addcontacts(name, number):
    query = "INSERT INTO contacts VALUES (NULL, ?, ?, 'null')"
    cursor.execute(query, (name, number))
    conn.commit()

def add_contact_from_query(user_query):
    """
    Extracts contact details from the user query and adds them to the database.
    """
    name, number = extract_contact_details(user_query)
    if name and number:
        cursor.execute("INSERT INTO contacts VALUES (NULL, ?, ?, 'null')", (name, number))
        conn.commit()
        print(f"Contact {name} with number {number} added successfully!")
        result = f"Contact {name} with number {number} added successfully!"
        speak(result)
    else:
        print("Invalid query format! Use: 'Add <Name> <PhoneNumber>'")
        result = "Invalid query format! Use: 'Add <Name> <PhoneNumber>'"
        speak(result)

def extract_contact_details(query):
    """
    Extracts name and phone number from the user input.
    Example: "Add John 9876543210"
    """
    match = re.search(r"add\s+([A-Za-z]+)\s+(\d{10})", query, re.IGNORECASE)
    if match:
        name = match.group(1)
        number = match.group(2)
        return name, number
    return None, None

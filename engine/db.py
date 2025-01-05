import sqlite3
 
conn = sqlite3.connect("Eleven.db")
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_commands(id integer primary key, name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)

# query = "UPDATE sys_commands set name =? WHERE id = ?"
# data =("ms edge",6)
# cursor.execute(query,data)
# conn.commit()

query = "CREATE TABLE IF NOT EXISTS web_commands(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)


# query = "INSERT INTO web_commands VALUES(null,'rgit college','https://www.mctrgit.ac.in/')"
# cursor.execute(query)
# conn.commit()
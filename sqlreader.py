import sqlite3

def read_from_db(db_path, query):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Create a cursor object
    c = conn.cursor()

    # Execute the query
    c.execute(query)

    # Fetch all the rows from the result of the query
    rows = c.fetchall()

    # Close the connection to the database
    conn.close()

    # Return the rows fetched
    return rows


# Define the path to the SQLite database
db_path = 'audio_files.db'

# Define the SELECT query
query = 'SELECT * FROM voice_transcriptions'

# Use the function to read from the database
rows = read_from_db(db_path, query)

# Print the rows fetched
for row in rows:
    print(row)


    
# Create the SQLite connection and cursor
# This is your database thread
def db_thread(q):
    conn = sqlite3.connect('audio_files.db')
    c = conn.cursor()
    c.execute("""
CREATE TABLE IF NOT EXISTS audio_files (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    access_time TEXT
)
""")
    conn.commit()
    c.execute("""
    CREATE TABLE IF NOT EXISTS voice_transcriptions (
        id INTEGER PRIMARY KEY,
        audio_filename TEXT,
        transcription TEXT
    )
    """)
    conn.commit()

    while True:
        request = q.get()  # Blocks until there is a request available
        if request is None:  # We send None to signal the database thread to end
            break

        operation, data, result_queue = request  # Unpack the request

        if operation == 'insert':  # Insert a new row
            mp3_path, transcript = data
            try:
                c.execute("""
                    INSERT INTO voice_transcriptions(audio_filename, transcription)
                    VALUES (?, ?)
                    """, (mp3_path, str(transcript),))
                conn.commit()
                if result_queue is not None:
                    result_queue.put('ok')  # Send back confirmation
            except sqlite3.Error as e:
                if result_queue is not None:
                    result_queue.put(e)  # Send back the error

        elif operation == 'select':  # Select data from the database
            query = data
            try:
                c.execute(query)
                rows = c.fetchall()
                if result_queue is not None:
                    result_queue.put(rows)  # Send back the result
            except sqlite3.Error as e:
                if result_queue is not None:
                    result_queue.put(e)  # Send back the error

    conn.close()


# Now we create the queue and the thread
db_requests = Queue()

# And start the thread
#db_worker.start()

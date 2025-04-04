import sqlite3  # Ensure this is at the top of your file

def save_message(sender, receiver, message):
    try:
        conn = sqlite3.connect("chatapp.db")  # Connect to the database
        cursor = conn.cursor()

        # Create the messages table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert the message into the table
        cursor.execute('''
            INSERT INTO messages (sender, receiver, message)
            VALUES (?, ?, ?)
        ''', (sender, receiver, message))

        conn.commit()  # Save changes
        conn.close()  # Close connection
        print("Message saved successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")


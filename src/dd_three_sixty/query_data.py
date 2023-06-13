import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM weather_data")

# Fetch all rows returned by the query
rows = cursor.fetchall()

# Process the fetched data
for row in rows:
    print(row)

# Close the database connection
conn.close()

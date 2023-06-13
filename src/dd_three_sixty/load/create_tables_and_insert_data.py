import sqlite3
import json
import os
import logging

def create_tables(cursor):
    # Create the cities table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE
                    )''')

    # Create the response_codes table
    cursor.execute('''CREATE TABLE IF NOT EXISTS response_codes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        code INTEGER UNIQUE
                    )''')

    # Create the weather_data table
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        run_identifier TEXT,
                        city_id INTEGER,
                        response_code_id INTEGER,
                        data JSON,
                        FOREIGN KEY (city_id) REFERENCES cities (id),
                        FOREIGN KEY (response_code_id) REFERENCES response_codes (id)
                    )''')

def insert_city(cursor, city_name):
    cursor.execute('INSERT OR IGNORE INTO cities (name) VALUES (?)', (city_name,))

def insert_response_code(cursor, code):
    cursor.execute('INSERT OR IGNORE INTO response_codes (code) VALUES (?)', (code,))

def insert_weather_data(cursor, run_identifier, city_id, response_code_id, data):
    cursor.execute('INSERT INTO weather_data (run_identifier, city_id, response_code_id, data) VALUES (?, ?, ?, ?)',
                   (run_identifier, city_id, response_code_id, json.dumps(data)))

def scrape_and_save_data():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    create_tables(cursor)

    raw_data_folder = '/data/raw_data/'

    # Create a logger
    logging.basicConfig(filename='data_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    # Iterate over the city folders
    for city_folder in os.listdir(raw_data_folder):
        city_folder_path = os.path.join(raw_data_folder, city_folder)
        if os.path.isdir(city_folder_path):
            # Iterate over the JSON files in the city folder
            for filename in os.listdir(city_folder_path):
                if filename.endswith('_response.json'):
                    try:
                        with open(os.path.join(city_folder_path, filename)) as file:
                            json_data = json.load(file)

                            # Get the city name and insert it into the cities table
                            city_name = city_folder
                            insert_city(cursor, city_name)

                            # Get the response code and insert it into the response_codes table
                            response_code = json_data['response_code']
                            insert_response_code(cursor, response_code)

                            # Insert the weather data into the weather_data table
                            run_identifier = json_data['run_identifier']
                            city_id = cursor.execute('SELECT id FROM cities WHERE name = ?', (city_name,)).fetchone()[0]
                            response_code_id = cursor.execute('SELECT id FROM response_codes WHERE code = ?', (response_code,)).fetchone()[0]
                            data = json_data['requested_data']
                            insert_weather_data(cursor, run_identifier, city_id, response_code_id, data)

                        conn.commit()
                        logger.info(f"Data from {filename} in {city_name} successfully processed and saved to the database.")
                    except Exception as e:
                        logger.error(f"Error processing data from {filename} in {city_name}: {str(e)}")

    conn.close()

if __name__ == '__main__':
    scrape_and_save_data()

## Weather Data ETL Summary

This summary provides an overview of the ETL (Extract, Transform, Load) steps involved in processing weather data using Airflow and Docker.

### Step 1: Scrape Weather Data

The first step in the ETL process is to scrape weather data from a website. This is accomplished using the `extract/scrape_cities.py` script. The script makes an HTTP request to the weather website, retrieves the HTML content, and extracts the required data using regular expressions. The scraped data is then saved as JSON files, with one file per city and run.

### Step 2: Load Data to SQL Database

After scraping the weather data, the next step is to load it into an SQL database. The `load/create_tables_and_insert_data.py` script connects to an SQLite database and creates tables for storing the scraped data. It reads the JSON files generated in the previous step, extracts the relevant information, and inserts it into the corresponding tables. The database design includes tables for cities, HTTP response codes, and the weather data itself.

### Step 3: Transform Data to Parquet Format

Once the data is successfully loaded into the SQL database, the `transform/to_parquet.py` script performs data transformation and writes the transformed data to Parquet files. The script retrieves the necessary information from the database, computes summary statistics for each city, and partitions the data based on the run identifier. The resulting Parquet files contain a summary of the information available in the database at the time of execution, including maximum, minimum, and average values, as well as the last update for each city.

### Technologies Used

The following technologies were used in the Weather Data ETL process:

- **Python:** The scripts for scraping, loading to SQL, and transforming to Parquet were written in Python, a versatile and widely-used programming language.
- **Regular Expressions:** Regular expressions were employed to extract data from the HTML content obtained during the scraping process.
- **SQLite:** The SQL database used for storing the weather data is SQLite, a lightweight and serverless database engine.
- **Airflow:** Airflow, a popular open-source platform, was utilized to orchestrate and schedule the ETL process. It provides task management, scheduling, and monitoring capabilities.
- **Docker:** Docker was used to containerize the Airflow environment, ensuring portability and ease of deployment across different systems.

# ETL Process: Weather Data Extraction, Loading, and Transformation

The ETL (Extract, Load, Transform) process consists of three main steps: scraping weather data, loading it into a SQL database, and transforming it into Parquet format. Each step plays a specific role in the overall data pipeline.

## 1. Extract (Scraper)

The first step is to extract weather data from a specific source. In this case, a web scraper is used to retrieve weather information from a website. The scraper accesses the webpage, extracts the relevant data using HTML parsing or regular expressions, and stores it in a structured format.

## 2. Load (SQL Script)

Once the data is extracted, it needs to be loaded into a SQL database for further processing and analysis. A SQL script is responsible for creating the necessary tables, establishing the database connection, and inserting the extracted data into the appropriate tables. The script ensures data integrity and handles any errors that may occur during the loading process.

## 3. Transform (Parquet Script)

After the data is loaded into the SQL database, it is transformed into the Parquet format. A Parquet script reads the data from the SQL tables, performs necessary transformations, calculations, and aggregations, and then writes the transformed data into Parquet files. The Parquet format offers efficient storage, compression, and columnar data organization, making it ideal for big data analytics and processing.

## Technologies Used

The ETL process incorporates the following technologies:

- **Python**: Used for web scraping, data processing, and scripting the ETL pipeline. Python provides a rich ecosystem of libraries and tools for data extraction, transformation, and loading.

- **Beautiful Soup**: A Python library for parsing HTML and XML data, used for web scraping in the extraction phase. Beautiful Soup makes it easy to navigate and extract data from HTML pages.

- **SQL**: Structured Query Language is used for creating and managing relational databases. SQL is used in the loading phase to define tables, establish connections, and insert data into the SQL database.

- **Parquet**: A columnar storage file format used for data transformation in the ETL process. Parquet offers efficient compression and serialization of data, making it well-suited for big data processing and analytics.

- **Docker**: Used for containerization and deployment of the ETL pipeline. Docker allows for easy packaging and distribution of applications, ensuring consistency across different environments.

- **Docker Compose**: A tool for defining and managing multi-container Docker applications. Docker Compose is used to orchestrate the MySQL database and Python services, enabling easy deployment and management of the ETL pipeline.

- **Airflow**: A platform for programmatically authoring, scheduling, and monitoring workflows. Airflow is used for orchestrating the sequential execution of the scraper, SQL load, and Parquet transformation scripts.

## Data Flow

The data flows through the ETL process as follows:

1. The Scraper extracts weather data from a website using Python and Beautiful Soup.
2. The SQL Script establishes a connection to the SQLite database and loads the extracted data using SQL statements.
3. The Parquet Script reads the data from the SQL database, performs transformations using Python, and writes the transformed data into Parquet files.

The sequential execution of these steps ensures a smooth flow of data from extraction to loading and transformation, leveraging the power of Python, SQL, SQLite3, Parquet, Docker, Docker Compose, and Airflow.

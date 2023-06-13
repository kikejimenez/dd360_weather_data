import sqlite3
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def generate_summary_data(conn):
    query = '''
        SELECT cities.name AS city_name,
               MAX(json_extract(weather_data.data, '$.temperature')) AS max_temperature,
               MIN(json_extract(weather_data.data, '$.temperature')) AS min_temperature,
               AVG(json_extract(weather_data.data, '$.temperature')) AS avg_temperature,
               MAX(json_extract(weather_data.data, '$.last_update')) AS last_update,
               weather_data.run_identifier AS run_identifier
        FROM weather_data
        JOIN cities ON weather_data.city_id = cities.id
        GROUP BY city_name
    '''

    summary_data = pd.read_sql_query(query, conn)
    return summary_data

def generate_parquet_file():
    conn = sqlite3.connect('weather_data.db')
    summary_data = generate_summary_data(conn)

    # Convert last_update column to datetime type
    summary_data['last_update'] = pd.to_datetime(summary_data['last_update'])
    output_dir = '/data/parquet_data/weather_summary.parquet'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Partition the data by run_identifier
    table = pa.Table.from_pandas(summary_data, preserve_index=False)
    pq.write_to_dataset(table, root_path=output_dir, partition_cols=['run_identifier'])

    conn.close()

if __name__ == '__main__':
    generate_parquet_file()

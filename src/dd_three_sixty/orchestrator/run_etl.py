from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'enrique',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('weather_data_pipeline', default_args=default_args, schedule_interval='@daily')

scrape_command = "python /python/src/dd_three_sixty/extract/scrape_cities.py"
load_command = "python /python/src/dd_three_sixty/load/create_tables_and_insert_data.py"
transform_command = "python /python/src/dd_three_sixty/transform/to_parquet.py"

with dag:
    scrape_task = BashOperator(
        task_id='scrape_weather_data',
        bash_command=scrape_command,
    )

    load_task = BashOperator(
        task_id='load_data_to_sql',
        bash_command=load_command,
    )

    transform_task = BashOperator(
        task_id='transform_to_parquet',
        bash_command=transform_command,
    )

    # Define the execution order of the tasks
    scrape_task >> load_task >> transform_task

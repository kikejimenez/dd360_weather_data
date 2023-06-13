FROM  apache/airflow:2.3.0

WORKDIR /wd

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /wd

# CMD ["python", "script_name.py"]
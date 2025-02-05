from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import requests

input_file = '/opt/airflow/data/web-server-access-log.txt'
extracted_file = '/opt/airflow/data/extracted-data.txt'
transformed_file = '/opt/airflow/data/transformed.txt'
output_file = '/opt/airflow/data/capitalized.txt'


def download_file():
    url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(input_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

def extract_file():
    global extracted_file
    with open(input_file, 'r') as infile, open(extracted_file, 'w') as outfile:
        for line in infile:
            fields = line.split('#')
            timestamp = fields[0]
            visitor_id = fields[3]
            outfile.write(timestamp + '#' + visitor_id + '\n')


def transform_data():
    global extracted_file, transformed_file
    with open(extracted_file, 'r') as infile, open(transformed_file, 'w') as outfile:
        for line in infile:
            processed_line = line.upper()
            outfile.write(processed_line)


def load_data():
    global output_file
    with open(transformed_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line)


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='My first ETL DAG',
    schedule=timedelta(days=1)
)

execute_download = PythonOperator(
    task_id='download_file',
    python_callable=download_file,
    dag=dag
)


execute_extract = PythonOperator(
    task_id='extract_data',
    python_callable=extract_file,
    dag=dag
)

execute_transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

execute_load = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

execute_download >> execute_extract >> execute_transform >> execute_load
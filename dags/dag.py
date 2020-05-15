import os
import requests
from contextlib import closing
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME')
BEAM_SRC_HOME = os.environ.get('BEAM_SRC_HOME')
OPEN_FOOD_FACTS_URL = 'https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv'
OUTPUTS_DIR = os.path.join(AIRFLOW_HOME, 'outputs')
OUTPUT_FILENAME = os.path.join(OUTPUTS_DIR, 'fr.openfoodfacts.org.products.csv')

default_args = {
    'owner': 'CGF',
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': days_ago(1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}


def fetch_dataset():
    with open(OUTPUT_FILENAME, 'w') as f_out:
        with closing(requests.get(OPEN_FOOD_FACTS_URL, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            for line in f:
                f_out.write(line)
                f_out.write('\n')


def verify_if_file_exists():
    if os.path.isfile(OUTPUT_FILENAME):
        return 'compile_and_run_pipeline'
    return 'fetch_dataset'


dag = DAG(
    'open-food-facts-DAG',
    default_args=default_args,
    description='Fetch, parse and concatenate results of Open Food Facts analysis',
    schedule_interval=None
)

verify_if_file_exists = BranchPythonOperator(
    task_id='verify_if_file_exists',
    python_callable=verify_if_file_exists,
    dag=dag,
)

fetch_dataset = PythonOperator(
    task_id='fetch_dataset',
    python_callable=fetch_dataset,
    dag=dag
)

compile_and_run_pipeline = DockerOperator(
    task_id='compile_and_run_pipeline',
    image='maven:3.6.3-jdk-11',
    auto_remove=True,
    command="/bin/bash -c \"ls -al . && mvn verify && \
    java -jar target/open-food-facts-nutrition-info-1.0-SNAPSHOT-jar-with-dependencies.jar \
    --inputFile=outputs/fr.openfoodfacts.org.products.csv\"",
    container_name='openfood',
    volumes=[
        BEAM_SRC_HOME + ':/usr/src/open-food-facts'
    ],
    working_dir='/usr/src/open-food-facts',
    trigger_rule='one_success',
    dag=dag,
)

concatenate_results = BashOperator(
    task_id='concatenate_results',
    bash_command='cd ' + OUTPUTS_DIR + ' && \
    cat open-food-facts-result-* > open-food-facts-final-result && \
    rm -rf open-food-facts-result-*',
    dag=dag,
)

verify_if_file_exists >> [fetch_dataset, compile_and_run_pipeline]
fetch_dataset >> compile_and_run_pipeline >> concatenate_results

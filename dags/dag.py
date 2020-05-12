import os
import requests
from contextlib import closing
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME')
DAGS_HOME = os.path.join(AIRFLOW_HOME, 'dags')
BEAM_SRC_HOME = os.environ.get('BEAM_SRC_HOME')
MVN_REPO = os.environ.get('MVN_REPO')
OPEN_FOOD_FACTS_URL = 'https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv'
OUTPUT_FILENAME = 'fr.openfoodfacts.org.products.csv'

default_args = {
    'owner': 'CGF',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}


def fetch_data():
    filename = os.path.join(DAGS_HOME, OUTPUT_FILENAME)
    with open(filename, 'w') as f_out:
        with closing(requests.get(OPEN_FOOD_FACTS_URL, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            for line in f:
                f_out.write(line)
                f_out.write('\n')


def verify_if_file_exists():
    filename = os.path.join(DAGS_HOME, OUTPUT_FILENAME)
    if os.path.isfile(filename):
        return 'docker'
    return 'fetch_data'


dag = DAG(
    'open-food-facts-DAG',
    default_args=default_args,
    description='Fetch, parse and concatenate results of Open Food Facts analysis',
    schedule_interval=None
)

branch_task = BranchPythonOperator(
    task_id='check_if_file_exists',
    python_callable=verify_if_file_exists,
    dag=dag,
)

t1 = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag
)

filename = os.path.join(DAGS_HOME, OUTPUT_FILENAME)

t2_temp = BashOperator(
    task_id='create_smaller_test_file',
    bash_command='cd ' + DAGS_HOME + ' && head -n 200 '+OUTPUT_FILENAME+ ' > test.csv',
    dag=dag
)

t2 = DockerOperator(
    task_id='docker',
    image='maven:3.6.3-jdk-11',
    auto_remove=True,
    command="/bin/bash -c \"ls -al . && mvn verify && \
    java -jar target/open-food-facts-nutrition-info-1.0-SNAPSHOT-jar-with-dependencies.jar \
    --inputFile=dags/test.csv\"",
    container_name='openfood',
    volumes=[
        BEAM_SRC_HOME+':/usr/src/open-food-facts',
        MVN_REPO+':/root/.m2'
    ],
    working_dir='/usr/src/open-food-facts',
    trigger_rule='one_success',
    dag=dag,
)

t3 = BashOperator(
    task_id='concatenate_results',
    bash_command='cd ' + DAGS_HOME + '/results && ls -al',
    dag=dag,
)

branch_task >> t1
branch_task >> t2
t1 >> t2_temp >> t2
t2 >> t3

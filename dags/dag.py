import os
import requests
from contextlib import closing
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME')
OPEN_FOOD_FACTS_URL = 'https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv'
OUTPUT_FILENAME = 'fr.openfoodfacts.org.products.csv'

default_args = {
    'owner': 'CGF',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


def fetch_data():
    filename = os.path.join(AIRFLOW_HOME, OUTPUT_FILENAME)
    with open(filename, 'w') as f_out:
        with closing(requests.get(OPEN_FOOD_FACTS_URL, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            for line in f:
                f_out.write(line)
                f_out.write('\n')


dag = DAG(
    'open-food-facts-DAG',
    default_args=default_args,
    description='Fetch, parse and concatenate results of Open Food Facts analysis',
    schedule_interval=None
)

t1 = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    dag=dag,
)

t2 = BashOperator(
    task_id='run_dataflow_job',
    bash_command='cd ' + AIRFLOW_HOME + ' && touch dataflow_dummy_file',
    dag=dag,
)

t3 = BashOperator(
    task_id='concatenate_results',
    bash_command='cd ' + AIRFLOW_HOME + ' && rm -rf dataflow_dummy_file',
    dag=dag,
)

t1 >> t2 >> t3

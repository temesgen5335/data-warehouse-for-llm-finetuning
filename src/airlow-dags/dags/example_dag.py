from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='test_hello_world',
    start_date=datetime(2024, 5, 23),
    schedule_interval='@daily',
    tags=['llm', 'dw', 'hello_world'],
) as dag:
    # Define task to test hello world
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Hello World"',
    )
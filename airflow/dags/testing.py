from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_python_dag',
    default_args=default_args,
    description='An example DAG with Python tasks',
    schedule_interval=timedelta(days=1),
)

# Define Python functions for tasks
def task_1():
    print("Executing Task 1")
    return "Task 1 completed"

def task_2(ti):
    task_1_result = ti.xcom_pull(task_ids='task_1')
    print(f"Received from Task 1: {task_1_result}")
    print("Executing Task 2")
    return "Task 2 completed"

def task_3(ti):
    task_2_result = ti.xcom_pull(task_ids='task_2')
    print(f"Received from Task 2: {task_2_result}")
    print("Executing Task 3")
    return "Task 3 completed"

# Create PythonOperator tasks
task_1 = PythonOperator(
    task_id='task_1',
    python_callable=task_1,
    dag=dag,
)

task_2 = PythonOperator(
    task_id='task_2',
    python_callable=task_2,
    dag=dag,
)

task_3 = PythonOperator(
    task_id='task_3',
    python_callable=task_3,
    dag=dag,
)

# Set task dependencies
task_1 >> task_2 >> task_3
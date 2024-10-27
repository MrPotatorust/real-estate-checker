from sqlalchemy import create_engine, text, insert

import logging
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

my_dag = DAG(
    dag_id = "Database_conn_test",
    default_args=default_args,
    description="Tests the database connections with sqlachemy",
    #schedule_interval=timedelta(days=1),
    schedule=None,
)


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def testing_staging_database():
    conn_vars = BaseHook.get_connection('staging_db')
    engine = create_engine(f'postgresql://{conn_vars.login}:{conn_vars.password}@{conn_vars.host}:{conn_vars.port}/{conn_vars.schema}')


    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM property_listings"))
        logger.info(result.all())


testing_staging_database = PythonOperator(
    task_id="scraping",
    python_callable=testing_staging_database,
    dag=my_dag,
)

testing_staging_database
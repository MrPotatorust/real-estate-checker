from datetime import datetime, timedelta

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from sqlalchemy import create_engine
import numpy as np
import pandas as pd



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
    dag_id = "Database_loader",
    default_args=default_args,
    description="Merges two databases",
    #schedule_interval=timedelta(days=1),
    schedule=None,
)




conn_vars_staging = BaseHook.get_connection('staging_db')
engine_staging = create_engine(f'postgresql://{conn_vars_staging.login}:{conn_vars_staging.password}@{conn_vars_staging.host}:{conn_vars_staging.port}/{conn_vars_staging.schema}', echo=True)

conn_vars_destination = BaseHook.get_connection('testing_scripts_main_testing_database')
engine_destination = create_engine(f'postgresql://{conn_vars_destination.login}:{conn_vars_destination.password}@{conn_vars_destination.host}:{conn_vars_destination.port}/{conn_vars_destination.schema}', echo=True)


def loading():
    staging_df_nehnutelnosti = pd.read_sql("SELECT * FROM property_listings_nehnutelnosti", con=engine_staging)
    staging_df_bazos = pd.read_sql("SELECT * FROM property_listings_bazos", con=engine_staging)

    frames = [staging_df_nehnutelnosti, staging_df_bazos]

    staging_df = pd.concat(frames)
    staging_df.to_sql("property_listings_merged", con=engine_destination, if_exists='replace')




loading = PythonOperator(
    task_id="loading_to_database",
    python_callable=loading,
    dag=my_dag,
)


loading
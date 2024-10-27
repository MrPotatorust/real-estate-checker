from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id = 'table_initialization',
    default_args = default_args,
    start_date = datetime(2023, 1, 1),
    schedule=None,
) as dag:
    bazos_table_creation = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = 'staging_db',
        sql="""
            CREATE TABLE IF NOT EXISTS property_listings (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                price NUMERIC(12, 2),
                sq_m INTEGER,
                img TEXT,
                link TEXT,
                location VARCHAR(255),
                postal_code VARCHAR(20),
                rentable BOOLEAN,
                property_type VARCHAR(50),
                site VARCHAR(100)
            );
        """
    )

    # Proper task flow
    bazos_table_creation
from airflow import DAG
import os
from datetime import datetime, timedelta
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.dummy import DummyOperator
from web.operators.fire.fireHKoperator import FireIncidentsToPostgresOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator


# Define your default arguments
default_args = {
    'owner': 'chinedu',
    'start_date': datetime(2023, 12, 1),
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

# Create your DAG
with DAG(
    'fire_incidents_dag', 
    default_args=default_args,
      schedule_interval=None) as dag:
    
    start = DummyOperator(task_id='start')

    # Fetch and store data in GCS
    extract_to_pg = FireIncidentsToPostgresOperator(
        task_id='download_to_pg',
        table='fire_incidents_data',  # Replace with your desired table name
        api_endpoint='https://data.sfgov.org/resource/wr8u-xric.json',
        api_headers={
            "X-App-Token": '', # add your app  token
            "X-App-Secret": '',   # add app secret
        },
        api_params={
            "$limit": 2000,
        },
    )


    # Load data from PostgreSQL to GCS
    get_data_gcs  = PostgresToGCSOperator(
        task_id='postgres_to_gcs',
        sql='SELECT * FROM fire_incidents_data',  # Replace with your SQL query
        postgres_conn_id='postgres_default',  # Replace with your PostgreSQL connection ID
        bucket ='ite-1',  # Replace with your GCS bucket name
        filename='fire/fire_incidents.csv',  # Replace with your desired file name
        schema= None,  # Replace with your PostgreSQL schema
        field_delimiter=',',
        export_format='CSV',
        dag=dag,
)

    # Push data from GCS to BigQuery
    upload_to_bigquery = GCSToBigQueryOperator(
        task_id='upload_to_bigquery',
        source_objects=['fire/fire_incidents.csv'],
        destination_project_dataset_table='capstone-407706.fire.fire_incidents_table',
        schema_fields=[],  # Define schema fields if needed
        skip_leading_rows=1,
        source_format='CSV',
        field_delimiter=',',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',  # Change to your desired write disposition
        autodetect=True, 
        bucket ='ite-1',
    )


    end = DummyOperator(task_id='end')

    # Define task dependencies
    start >> extract_to_pg >> get_data_gcs >> upload_to_bigquery >> end
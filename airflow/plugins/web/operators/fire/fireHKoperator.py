# Import necessary modules
import time
import json
from typing import Dict, Any, Optional, Sequence, Union
from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
import requests
from datetime import timedelta

class FireIncidentsToPostgresOperator(BaseOperator):

    def __init__(
        self,
        api_endpoint: str,
        api_headers: Dict[str, str],
        api_params: Dict[str, Union[str, int]],
        table: str = "fire_incidents_data",
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.api_endpoint = api_endpoint
        self.api_headers = api_headers
        self.api_params = api_params
        self.table = table
    

    def execute(self, context):
        
        # Make an authenticated GET request to the API
        try:
            response = requests.get(self.api_endpoint, params=self.api_params, headers=self.api_headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error(f"Error during data download: {e}")


        if response.status_code == 200:
            # Convert the response JSON to a DataFrame
            df = pd.DataFrame(response.json())

        # SQLAlchemy logic to send data to PostgreSQL
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
        engine = postgres_hook.get_sqlalchemy_engine()
        df.to_sql(name=self.table, con=engine, index=False, if_exists="replace",dtype=sqlalchemy.types.JSON)
        self.log.info("Table successfully loaded")
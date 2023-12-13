## An ELT Data Pipeline for the San Francisco fire incidents

## Project scope

This project aims at building an Extract, Load, Transform (ELT) data pipeline using the San Francisco fire incidents dataset via the API.The dataset can be accessed from the open data portal https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric/about_data . The pulled data is then loaded into a PostgreSQL database, move to Google Cloud Storage (GCS) bucket, and then to a data warehouse(BigQuery). From BigQuery, the data can be transformed using dbt and finally visualize using any BI tool like looker, Power BI , e.t.c.

The image below shows the flow of the project:

![image](https://github.com/eduonyia/fire_incidents_elt_project/assets/6407387/805dd8b2-c370-4fe0-b2f6-f51458d44b2d)




## Dataset Description

- **Name:** Fire Incidents
- **Category:** Public Safety
- **Data Source:** San Francisco 
- **Rows:** 648K
- **Columns:** 64
- **Description:** Fire Incidents includes a summary of each (non-medical) incident to which the SF Fire Department responded. Each incident record includes the call number, incident number, address, number and type of each unit responding, call type (as determined by dispatch), prime situation (field observation), actions taken, and property loss.
- **Data Dictionary:** [FIR-0001_DataDictionary_fire-incidents.xlsx](https://github.com/eduonyia/fire_incidents_elt_project/files/13657247/FIR-0001_DataDictionary_fire-incidents.xlsx)


# Project Milestones

## Milestone 1- Data Extraction and Loading (Extract and Load Pipeline)

### Code Explanation

This code defines a custom Airflow Operator (`FireIncidentsToPostgresOperator`) responsible for extracting data from the San Francisco Fire Incidents dataset API and load it into a PostgreSQL database.The key components of the custom Airflow Operator are:

- **Initialization:**
  - The python constructor (`__init__` method) initializes the parameters, including the API details, PostgreSQL connection ID and table name.

- **Execution Method (`execute`):**
  - Constructs the API URL based on the provided endpoint.
  - Sets up parameters for the API request, including table name.
  - Sends a GET request to the API with proper headers and parameters.
  - Performs error handling on the API response and converts the JSON data to a Pandas DataFrame if the response is successful (status code 200)
  - Writes the Pandas DataFrame to a PostgreSQL database table using the PostgresHook and SQLAlchemy


## Milestone 2- Data Transformation and Integration (ELT Pipeline):

A PostgresToGCSOperator Operator is used to transfer data from the PostgreSQL database table to Google Cloud Storage (GCS) bucket
and later loaded to Google BigQuery for further analysis.

### Tools and Definitions

This section explains some tools and keywords used in this project.

- **Docker:**
  - Docker is a platform designed to help developers build, share, and run container applications. Docker handles the tedious setup, so you can focus on the code.

- **Airflow:**
  - Apache Airflow is an open-source workflow management platform for data engineering pipelines.

- ** Directed Acyclic Graph (`dag`):**
  - is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies. A DAG is defined in a Python script, which represents the DAGs structure (tasks and their dependencies) as code.

- **Tasks:**
  - A Task is the basic unit of execution in Airflow. Tasks are arranged into DAGs, and then have upstream and downstream dependencies set between them into order to express the order they should run in
  - `start_task`: A dummy task marking the start of the DAG.
  - `extract_to_pg`: Task representing the data extraction and loading of data to the PostgreSQL.
  - `get_data_gcs`: Task representing the transfer of data from the PostgreSQL to the GCS bucket.
  - `upload_to_bigquery`: Task representing the loading of data to the Data Warehouse(Google BigQuery).
  - `end_task`: Another dummy task marking the end of the DAG.

- **Task Dependencies (`start >> extract_to_pg >> get_data_gcs >> upload_to_bigquery >> end`):**
  - Specifies the order in which tasks should be executed.

- **Data Source:**
  - A data source is the location where data that is being used originates from. In this prject, the data sourse is open data API (San Francisco Fire Incidents data).

- **PostgreSQL:**
  - A free and open-source RDBMS.
   
- **Google Cloud Storage (`GCS`):**
  - Google Cloud Storage is a RESTful online file storage web service for storing and accessing data on Google Cloud Platform infrastructure.

- **Google BigQuery (`BigQuery`):**
  - BigQuery is Google's fully managed, serverless data warehouse that enables scalable analysis over petabytes of data.


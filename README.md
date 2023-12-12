## To create an ELT Data Pipeline for the San Francisco fire incidents

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
- **Description:** Fire Incidents includes a summary of each (non-medical) incident to which the SF Fire Department responded. Each incident record includes the call number, incident number, address, number and type of each unit responding, call type (as determined by dispatch), prime situation (field observation), actions taken, and property loss


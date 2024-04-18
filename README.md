# Overwatch League Stats

## Background

Overwatch is a first-person shooter team game with with a wide variety of heroes to choose from. [Overwatch League (OWL)](https://overwatchleague.com/en-us/news/23303225) was the professional esports league of Overwatch. I really enjoyed watching the OWL games since start, and have compiled and uploaded the game match stats to my [Kaggle](https://www.kaggle.com/datasets/sherrytp/overwatch-league-stats-lab). After initially struggling with analyzing vast amounts of stock data, I eventually shifted focus to illustrating the data engineering process using smaller datasets. This approach effectively showcases the orchestration of diverse data sources.

The datasets, originally provided by IBM Watson, include players, head-to-head match-ups, and maps. The player historical statistics should contain OWL games from 2018 till now. It's centered around each player, and player's picked hero, its team name, performance, match IDs, etc.


## Pre-requisites
- Install [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/install) (Windows Subsystem for Linux) on Windows
- Install Python (py3.10 above used for the project)
- Install VSCode
- [Install Docker Desktop](https://docs.docker.com/desktop/windows/install/)
- Have a Google Cloud Platform account
- [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk#deb) for Ubuntu

-  Infrastructure as Code: [Terraform](https://www.terraform.io/downloads/)
- Workflow Orchestration: [Mage]
- Data Lake: [Google Cloud Storage](https://cloud.google.com/storage)
- Data Warehouse: [Google BigQuery](https://cloud.google.com/bigquery)
- Batch Processing: [Spark](https://spark.apache.org/) on [Dataproc](https://cloud.google.com/dataproc)
- Visualisation: [Google Data Studio](https://datastudio.google.com/)


### Create a Google Cloud Project
1. Go to [Google Cloud](https://console.cloud.google.com/) and create a new project. The default project id is `project-stocks`. 
2. Go to IAM and [create a Service Account](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account) with these roles:
    - BigQuery Admin
    - Compute Admin
    - Storage Admin
    - Storage Object Admin
    - Viewer
3. Download the Service Account credentials and put inside the `terraform` folder.
4. On the Google console, enable the following APIs:
    - IAM API
    - IAM Service Account Credentials API
    - Cloud Dataproc API
    - Compute Engine API

### Set up the infrastructure with Terraform on Google Cloud Platform

1. Open the project folder in VSCode with WSL
2. Open `variables.tf` and modify:
    * `variable "project"` to your own project id, maybe not neccessary
    * `variable "region"` to your project region
    * `variable "credentials"` to your credentials path
3. Open the terminal in VSCode and change directory to terraform folder: `cd terraform` 
4. Initialize Terraform: `terraform init`
5. Plan the infrastructure: `terraform plan`
6. Apply the changes: `terraform apply`

If everything goes right, you now have a bucket on Google Cloud Storage called '<your_project>' and a dataset on BigQuery called ''.

### Airflow Optional

### Big Query Analytics

### dbt 
optional to keep local files with docker

### Spark ETL jobs
### visual
[visuals.png]

1. pie chart of maps
2. most dmg by player
3. max elim per game (vs total) by hero


### 404 Data not found error
* Mage - Error: "404 Not found: Dataset <dataset_name> was not found in location <your_location>

* DBT - Error: “404 Not found: Dataset <dataset_name>:<dbt_schema_name> was not found in location <your_location>” after building from stg_green_tripdata.sql

In the step in this video (DE Zoomcamp 4.3.1 - Build the First dbt Models), after creating `stg_green_tripdata.sql` and clicking `build`, I encountered an error saying dataset not found in location EU. The default location for dbt Bigquery is the US, so when generating the new Bigquery schema for dbt, unless specified, the schema locates in the US. 

Solution: 
Turns out I forgot to specify Location to be `EU` when adding connection details. 

Develop -> Configure Cloud CLI -> Projects -> taxi_rides_ny -> (connection) Bigquery -> Edit -> Location (Optional) -> type `EU` -> Save


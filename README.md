# streaming-r-stocks


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


## Background

1. 
2. Get a QUANDL API
3. Replace `mage-zoomcamp/data_loaders/read_api_data.py` with a simplier way is to use on a sample data: 
```
quandl.ApiConfig.api_key = 'yourquandlapi'
quandl.get_table('SHARADAR/DAILY', paginate=False)
```
4. `paginate` setting to False means the API calls will limit to 10,000 rows of data, but you should have enough sample data to understand the rest steps of the project. 
5. Attribute Definations Breakdown for QUANDL API. 

#### file 
    - **link​** ­ The string URL where the file can be downloaded, or null, if it is not present 
    - **status**​ The string status of the requested file; the possible values are: 
        - **Fresh** ­ the file is available and up to date 
        - **Creating** ­ the file is not available but it is bein created 
        - **Regenerating** ­ the file is available but it is out of date and a new one is being created 
    - **data_snapshot_time​** ­ the DateTime when the file creation process was initiated 
#### datatable
    - **last_refreshed_time​** ­ The DateTime when the table was last updated 
    > The generated ​link is only valid for 30 minutes. If your link expires, repeat your API call to generate a new ​download link. 


## Steps

### Create a Google Cloud Project
1. Go to [Google Cloud](https://console.cloud.google.com/) and create a new project. The default project id is `project-stocks`. 
2. Go to IAM and [create a Service Account](https://cloud.google.com/docs/authentication/getting-started#creating_a_service_account) with these roles:
    - BigQuery Admin
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

If everything goes right, you now have a bucket on Google Cloud Storage called 'datalake_<your_project>' and a dataset on BigQuery called 'stocks_data'.


### Spark ETL jobs

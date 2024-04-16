# Setting up a GCS bucket using Terraform

This is a walk-through guide for setting up a Google Cloud Storage (GCS) bucket using Terraform. 

## Prerequisites

Before you begin, you will need to have the following: 
- A Google Cloud Platform (GCP) account and create a project
- The `gcloud` command-line tool installed and authenticated with your GCP account/project
- The Terraform CLI installed in local machine

The infrastructure we will need consists of a Cloud Storage Bucket `google_storage_bucket` for our Data Lake and a BigQuery Dataset `google_bigquery_dataset`. 

## Files 

1. Clone the repository to your local machine. 
2. Open the project folder and avigate to the `terraform` directory. 
3. We will now create a new `main.tf` file as well as an auxiliary `variables.tf` file with all the blocks we will need for the project. 
4. Keep [`main.tf`](./main.tf) as what it is. 
5. Open [`variables.tf`](./variables.tf) and modify the following to your own account:
    ```
    variable "credentials" {
    description = "My Credentials"
    default     = "<Path to your Service Account json file>"
    #ex: if you have a directory where this file is called keys with your service account json file
    #saved there as my-creds.json you could use default = "./keys/my-creds.json"
    }


    variable "project" {
    description = "Project"
    default     = "<Your Project ID>"
    }

    variable "region" {
    description = "Region"
    #Update the below to your desired region
    default     = "<your-closet-region>"
    }

    variable "location" {
    description = "Project Location"
    #Update the below to your desired location
    default     = "US"
    }

    variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    #Update the below to what you want your dataset to be called
    default     = "demo_dataset"
    }

    variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    #Update the below to a unique bucket name
    default     = "terraform-demo-terra-bucket"
    }

    variable "gcs_storage_class" {
    description = "Bucket Storage Class"
    default     = "STANDARD"
    }
    ```
6. Execute and create the environment using the following commands. 

If everything goes right, you now have a bucket on Google Cloud Storage called 'datalake_<your_project>' and a dataset on BigQuery called 'owl_data'.

## Execution steps
1. `terraform init`:
    - Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control. 
2. `terraform plan`:
    - Matches/previews local changes against a remote state, and proposes an Execution Plan.
3. `terraform apply`:
    - Asks for approval to the proposed plan, and applies changes to cloud. 
4. `terraform destroy`:
    - Removes your stack from the Cloud. 
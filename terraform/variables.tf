variable "credentials" {
  description = "My Credentials"
  default     = "./radiant-arcanum-413707-d6bbe40a27e3.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}


variable "project" {
  description = "project-stocks"
  default     = "radiant-arcanum-413707"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "us-west1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name that raw data from GCS will be written to"
  #Update the below to what you want your dataset to be called
  default     = "owl_data"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "owl-match-stats"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
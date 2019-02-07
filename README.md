# Helpers

Common utility functions across IntelliMind projects

## Modules

### icalender
* **get_prior_business_day()** ::
It will return prior working business day with reference to today
* **get_today()** ::
It will give today's date
* **adjust_today(year, month, day)** ::
It will return today's date adjusted with given year, month, and day

### connections
* **get_mysql_connection(config)**
* **get_arctic_store(config)**
* **get_rethink_connection(config)**
* **get_dataframe_client(config)**
* **get_dataframe_hist_client(config)**

### aws.s3
* **upload_to_s3(bucket_name, local_source_path, remote_target_path, is_dir=False)**
	
	Uploading given file to s3 bucket

	Parametes :
	* local_source_path : local path of file or files in directory for input
	* remote_target_path : remote s3 bucket path of file / directory to store
	* bucekt_name : name of bucket in s3 that should exist
	* is_dir : is given local_source path is of directory ? (True / False)

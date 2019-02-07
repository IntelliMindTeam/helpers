# common-utils

Common utility functions across IntelliMind projects

## Modules

### icalender
* **get_prior_business_day()** ::
It will return prio working business day with reference to today**
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

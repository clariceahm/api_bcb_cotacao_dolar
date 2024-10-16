# Introduction
This project automates the process of retrieving the previous day's USD exchange rate, storing it in a database, and sending an email with the rate to specified recipients. It can be scheduled to run daily, making it ideal for businesses or individuals who require regular currency updates.

The Brazilian Central Bank API is available at the following endpoint: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/[resource_code]?$format=json&[Other_Parameters]

For detailed API documentation, refer to: https://dadosabertos.bcb.gov.br/dataset/dolar-americano-usd-todos-os-boletins-diarios/resource/ae69aa94-4194-45a6-8bae-12904af7e176

It is possible to retrieve the USD exchange rate for a specific day or over a date range. However, this project focuses on fetching the exchange rate for a single day (the previous day).

# Data Flow
The data flow in this project follows these steps:

Fetch the previous day's USD exchange rate using an API request to the aforementioned endpoint.
Store the fetched exchange rate in a SQL Server database table.
Send the exchange rate information via email using the SMTP protocol.
All these steps are orchestrated by running the main.py script. However, each step is handled by auxiliary scripts dedicated to specific tasks. Below is a description of each file's role within the project:

* connect_bd.py: Handles the connection to the SQL Server database and performs two functions: querying data (returning a DataFrame) and inserting data from a DataFrame into a database table.

* credentials_bd.txt: Stores the database access credentials. This file needs to be updated when cloning the project. You must provide the database server, database name, user, and password.

* email_account.txt: Stores the email account information used to send exchange rate notifications. In this project, Outlook was used as the email service. If you are using a different email service, you need to adjust the server_name key to match your chosen provider.

* extract_api.py: Makes the request to the Brazilian Central Bank API. The input to this script is the API URL, already containing the required query parameters.

* recipient_list.txt: Stores the list of email recipients who will receive the USD exchange rate information.

* send_email.py: Sends the email using the SMTP protocol.

* main.py: Serves as the main controller, coordinating the execution of the other scripts into a single routine.



# Installation

To run the project locally, follow the instructions below:

Clone the repository: git https://github.com/clariceahm/api_bcb_cotacao_dolar
Navigate to the project directory: cd yourrepository
Install the dependencies: pip install -r requirements.txt
After installation, you can run the included scripts to perform analyses. The results will be saved in output files or displayed in charts, depending on the script used.
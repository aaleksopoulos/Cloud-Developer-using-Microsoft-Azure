# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost ($) |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* | basic compute, 1 vcore, 5 GB storage   |     25.32       |
| *Azure Service Bus*   |    basic, 1 mil. operations     |      0.05        |
| *Azure Function App Service Plan*              |   Linux, B1   |     13.14         |
| *Azure Function App Storage Account*              |   general purpose v1  (100 tu)   |      2.44        |
| *Azure Web App*                | Free tier        | 0.00             |
| *SendGrid*                | Essential Plan        | 29.95             |

For extra information or alternatives about Microsoft Azure products [Pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/) can be used.
About SendGrid, and since it is a test environment, I assumed that the Free Plan with 100 emails per day will be sufficient for testing purposes.
Another issue that we should take into consideration is the fact that the above cost is based on the current (test) environment. If we want to move it to production environment, the cost would increase. With some basic assumptions, the following table could be a nice starting point

| Azure Resource | Service Tier | Monthly Cost ($) |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* | Single Server Deployment, General Purpose Tier, 1 Gen 5 (2 vCore)  50 GB Storage, 100 GB Additional Backup storage  |     143.65      |
| *Azure Service Bus*   |    Standard, 1 mil. operations     |     9.81       |
| *Azure Function App Service Plan*              |   Linux, B1   |     13.14         |
| *Azure Function App Storage Account*              |   Block Blob Storage, General Purpose V2, LRS Redundancy, Hot Access Tier, 100 GB Capacity - Pay as you go, 10 x 10,000 Write operations, 10 x 10,000 List and Create Container Operations, 10 x 10,000 Read operations, 1,00,000 Archive High Priority Read, 1 x 10,000 Other operations. 1,000 GB Data Retrieval, 1,000 GB Archive High Priority Retrieval, 1,000 GB Data Write   |     3.12        |
| *Azure Web App*                | Standard Tier; 1 S1 (1 Core(s), 1.75 GB RAM, 50 GB Storage); Linux OS     | 69.35             |
| *SendGrid*                | Essential Plan        | 29.95             |

About SendGrid, and since it is a conference, I assumed that the limit of the Essential Plan with 100.000 emails per month will be sufficient. 

## Architecture Explanation
Sending e-mails, especially to a potentially large number of attendees, could be a timely process, since we are looping over the total number of attendees. It would not be advisable for that duration the main site to be offline, or to risk http timeouts to happen. For that reason, the initial app was refactored and a Service Bus Queue was used. The main site keeps working as expected, while the notification sent part is handed over the bus queue to process the sending of the notifications. One other benefit of that modular approach (decoupling the web app from the sending notification part), has one extra benefit. Each process can be deployed and/or updated (in the aspect of bug elimination or adding new features), so separate teams can work in each part of the whole project.

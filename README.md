# Deloton-Project

![DelotonLogo](https://user-images.githubusercontent.com/115073814/217207897-f7b979af-dc1f-4fa5-89e4-99ee7c6a37c8.png)

Hello and welcome to The Three Musketeer's data pipeline, built to deliver a user interface for Deloton customers as well as a data warehoue for Deloton employees to access using an API and Tableau. The CEO of Deloton also receives a Daily Report.

## Table of contents

- [General Info](#general-info)
- [Project Roadmap](#project-roadmap)
- [Usage](#usage)
  - [Live Dashboard](#live-dashboard)
  - [RESTful API](#restful-api)
  - [Daily Report](#daily-report)
  - [Email Alerts](#email-alerts)
  - [Tableau Dashboard](#tableau-dashboard)
- [Credits & Acknowledgments](#credits-and-acknowledgements)
- [Further Development](#further-development)
- [Ways to Contribute](#ways-to-contribute)
- [Legacy Contributions](#legacy-contributions)

## General Info

This repo contains everything required to build a full ETL pipeline which collects data from live bike ride outputs and returns meaningful and insightful forms of data visualisation and functionality in the form of 5 key deliverables:

- Real-time dashboard display of current user ride and recent ride history
- Automated email service for excessively high heart rate
- Long term storage of user data for prospective business analysis
- Automated daily report summarising key metrics
- RESTful API
- Tableau integration to perform data querying and dashboard creation

## Project Roadmap

![Screenshot_Excalidraw](https://user-images.githubusercontent.com/115073814/217223449-26e6a315-d01c-4a11-a743-ceee6c4e60d7.png)

### Summary of above roadmap

1. Kafka consumer polls the Deloton topic receiving two logs per second.
2. Combines the two logs into one containing all the data for that second of the ride. Passes into SQLite table ready for querying from the Live Dashboard. Also creates user information table to store the current users details
3. When user heart rate exceeds heart rate limit during the ride, calculated as a function of the user's age, email alert sent using Amazon simple email service (SES)
4. At the end of the current ride, two csv files (user_info & ride_info) sent to s3 bucket. Tables are wiped for the next ride's data
5. AWS Lambda function reads csv files from s3 bucket and extracts key metrics (using Pandas) for long term storage in AWS RDS PostgreSQL table
6. RDS comprised of two tables, users and rides, joined by user_id
7. Tableau dashboard connected to RDS schemas and visuals created from it, live streaming the information
8. API hosted using AWS API Gateway, integrated with AWS Lambda Functions
9. Daily report hosted on AWS Lambda, extracting key metrics and formatted as an insightful summary, ran daily using Crontab

## Usage

### Live Dashboard

1. You will find the live dashboard up and running here: [Live Dashboard](http://18.130.141.140:8080/)
2. Top left button allows user to switch between viewing the current ride (user details along with their current performance) and recent ride details.
   If you would like to host run the dashboard yourself:

- Create your own EC2 instance and run the following commands
  NOTE: python3.10 is required for the most up to date version of pandas. The link to install this new version into your EC2 instance can be found [here](https://techviewleo.com/how-to-install-python-on-amazon-linux-2/)
  - `sudo yum install git`
  - `sudo git clone git@github.com:sebjshaw/Deloton-Project.git`
  - `cd Deloton-Project`
  - `sudo pip3.10 install -r requirements.txt`
  - `sudo amazon-linux-extras install redis6`
  - `sudo pip3.10 install sqlalchemy`
  - `sudo pip3.10 install psycopg2-binary`
  - `./run_files.sh`

#### Current Ride

<img width="1411" alt="Screenshot_LiveDashboard" src="https://user-images.githubusercontent.com/115073814/217261046-79872c89-567d-4f6e-bf45-7550f1fbcbdf.png">

#### Recent Rides

<img width="1414" alt="Screenshot_LiveDashboardRecent" src="https://user-images.githubusercontent.com/115073814/217261372-560e20da-d1ef-4a44-8d4f-6825283be560.png">

### RESTful API

[API](https://jzrx9wfk25.execute-api.eu-west-2.amazonaws.com/) can search the following endpoints:

`GET` `/ride/:id`
Get a ride with a specific ID

`GET` `/rider/:user_id`
Get rider information (e.g. name, gender, age, avg. heart rate, number of rides)

`GET` `/rider/:user_id/rides`
Get all rides for a rider with a specific ID

`DELETE` `/ride/:id`
Delete a with a specific ID

`GET` `/daily`
Get all of the rides in the current day

`GET` `/daily?date=01-01-2020`
Get all rides for a specific date

![Screenshot_API](https://user-images.githubusercontent.com/115073814/217295721-d7c80429-1267-4095-b8b6-67b73a49f0e4.png)

![Screenshot_API2](https://user-images.githubusercontent.com/115073814/217295783-d2d7a3f8-cba7-48f2-913a-ff723081caa1.png)

### Daily Report

16:45 every day, daily report is generated and sent off to the Deloton CEO's email detailing main findings over the last 24 hours.
Included in email as a link to index.html page which contains links to all historic daily reports. The index.html and daily reports are on an s3 bucket which acts as a host for the page. The most recent daily report is at the top.
Automated using Crontab

<img width="435" alt="daily_reportoooo" src="https://user-images.githubusercontent.com/115073814/217875230-8b640656-a526-4593-bcbc-29b06380c902.png">

### Email Alerts

1. EC2 hosting Kafka data stream automatically alerts user when their heart rate exceeds a certain level
2. Heart Rate Level calculated by age
3. Currently, emails sent to this address: three.musketeers.deloton@gmail.com

![Screenshot_Email](https://user-images.githubusercontent.com/115073814/217221056-2253c7c2-8ace-41bc-91f5-7f412795570c.png)

### Tableau Dashboard

1. Create a Tableau Cloud account if not done already ([Tableau](https://www.tableau.com/tableau-login-hub)).
2. Following link to [Deloton-Project](https://prod-uk-a.online.tableau.com/t/threemusketeers/views/safe-copy/Dashboard-RidesCompleted) prompts a login with AWS RDS credentials. Postgres account login details provided on day of presentation.
3. Dashboard consists of eight pages, each of which a leaderboard for the top users for that measured metric i.e. Number of rides completed by user, Highest average heart rate per ride per user.
4. User may navigate via the buttons on the righthand side of each page
5. Filters by gender, minimum & maximum value, and date of ride for interactability

![Screenshot_Tableau](https://user-images.githubusercontent.com/115073814/217216401-ccf2e62f-8258-485f-9d56-18a5df5a5859.png)

## Credits and Acknowledgements

Direct contributors to the repository:

- Seb Shaw: [sebjshaw](https://github.com/sebjshaw)
- Dominic Lawson: [DomLaw82](https://github.com/DomLaw82)
- Alexander Skowronski: [AlexSkowronski2](https://github.com/AlexSkowronski2)

Resources used:

- [Pandas](https://pandas.pydata.org/)
- [Amazon Web Services](https://aws.amazon.com/)
  - API Gateway
  - EC2
  - ECR
  - Lambda
  - S3
  - RDS
  - SES
- [Tableau Cloud](https://www.tableau.com/en-gb/products/cloud-bi)

## Further Development

Suggestions for additional features

### Live Dashboard Development

- Button to change the theme of the dashboard between light-mode and dark-mode
- Backtrack kafka logs to find user info when starting the EC2 middway through a ride

### API Development

- Authentication layer

### Daily Report Development

- Customise the summary in the report to be a bespoke overview of that specific days metrics and insights.
- Have a !!WARNING!! at the top of the page if there are more than 5 heart rate emails sent in one day

### Email Alerts Development

- Having a dedicated email address for sending heart rate exceeding limit email to a user's email that they have verified.

### Tableau Dashboard Development

- Age bin filter on Tableau dashboard for filtering specific ages of users, suggested bins could be: under 18s, 18-25, 25-35, 35-45, 45-55, over 55s
- Perhaps adding in resistance dashboard onto Tableau dashboard
- Parse through postcodes of users and have a map indicating where a current ride is happening or heat map of existing ride locations

## Ways to Contribute

1. Clone repo and create a new branch: `bash $ git checkout https://github.com/alichtman/stronghold -b name_for_new_branch`
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes

## Legacy Contributions

Welcome to the first edit - Alex
Another edit - this time Seb

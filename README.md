![DelotonLogo](https://user-images.githubusercontent.com/115073814/217207897-f7b979af-dc1f-4fa5-89e4-99ee7c6a37c8.png)

# Deloton-Project

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
- [Legacy Contributions](#legacy-contributions)

## General Info

Creation of a full ETL pipeline whereby data collected from live bike usage outputs meaningful and insightful forms of data visualisation and functionality.
These take the form of:

- Real-time dashboard display of current user ride and recent history
- Automated email service for excessively high heart rate data
- Long term storage of user data for prospective business analysis
- Automated daily report builder summarising key metrics
- RESTful API
- Tableau integration to perform data querying and dashboard creation

## Project Roadmap

![Screenshot_Excalidraw](https://user-images.githubusercontent.com/115073814/217223449-26e6a315-d01c-4a11-a743-ceee6c4e60d7.png)

### Summary of above roadmap:

1. Kafka Consumer in EC2 takes logs from Kafka Data stream every second
2. Parses through logs and cleans data, passes into SQLite table ready for querying for Live Dashboard, displays information on current ride and recent rides
3. At any point cleaned data suggests current user exceeds heart rate limit during ride, email alert trigger sent using Amazon simple email service (SES)
4. For a given ride for a specific user, at the end of their current ride, two csv files (user_info & ride_info) sent to s3 bucket (file storage service)
5. AWS Lambda function reads csv files from s3 bucket and extracts key metrics (using Pandas) for long term storage in AWS RDS postgres table
6. RDS comprised of two tables, users and rides, joined by user_id
7. Tableau dashboard connected to RDS schemas and visuals created from it, live streaming the information
8. API hosted on EC2 performing SQL queries from RDS
9. Daily report hosted on AWS Lambda, extracting key metrics and formatted as an insightful summary, ran daily using Crontab

## Usage

### Live Dashboard

1. You will find the live dashboard up and running here: [Live Dashboard](http://18.130.141.140:8080/)
2. Top left button allows user to switch between viewing the current ride (user details along with their current performance) and recent ride details.

<img width="1411" alt="Screenshot_LiveDashboard" src="https://user-images.githubusercontent.com/115073814/217261046-79872c89-567d-4f6e-bf45-7550f1fbcbdf.png">

### RESTful API

### Daily Report

### Email Alerts

1. EC2 hosting Kafka data stream automatically alerts user when their heart rate exceeds a certain level
2. Heart Rate Level calculated by age and weight
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

## Further Development

- Having a dedicated email address for sending heart rate exceeding limit email to a user's email that they have verified.
- Age bin filter on Tableau dashboard for filtering specific ages of users, suggested bins could be: under 18s, 18-25, 25-35, 35-45, 45-55, over 55s
- Perhaps adding in resistance dashboard onto Tableau dashboard 

## Legacy Contributions

Welcome to the first edit - Alex
Another edit - this time Seb

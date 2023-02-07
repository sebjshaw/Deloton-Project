![DelotonLogo](https://user-images.githubusercontent.com/115073814/217207897-f7b979af-dc1f-4fa5-89e4-99ee7c6a37c8.png)

# Deloton-Project

## Table of contents

- [General Info](#general-info)
- [Technologies](#technologies)
- [Setup](#setup)
- [Credits](#credits)
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

## Usage

### Heart Rate Email Alerts

1. EC2 hosting Kafka data stream automatically alerts user when their heart rate exceeds a certain level
2. Heart Rate Level calculated by age and weight
3. Currently, emails sent to this address: [three.musketeers.deloton@gmail.com](three.musketeers.deloton@gmail.com)

### Tableau Dashboard

1. Create a Tableau Cloud account if not done already ([Tableau](https://www.tableau.com/tableau-login-hub)).
2. Following link to [Deloton-Project](https://prod-uk-a.online.tableau.com/t/threemusketeers/views/safe-copy/Dashboard-RidesCompleted) prompts a login with AWS RDS credentials. Postgres account login details provided on day of presentation.
3. Dashboard consists of eight pages, each of which a leaderboard for the top users for that measured metric i.e. Number of rides completed by user, Highest average heart rate per ride per user.
4. User may navigate via the buttons on the righthand side of each page
5. Filters by gender, minimum & maximum value, and date of ride for interactability

![Screenshot_Tableau](https://user-images.githubusercontent.com/115073814/217216401-ccf2e62f-8258-485f-9d56-18a5df5a5859.png)

## Credits

Direct contributors to the repository:

- Seb Shaw: [sebjshaw](https://github.com/sebjshaw)
- Dominic Lawson: [DomLaw82](https://github.com/DomLaw82)
- Alexander Skowronski: [AlexSkowronski2](https://github.com/AlexSkowronski2)

## Legacy Contributions

Welcome to the first edit - Alex
Another edit - this time Seb

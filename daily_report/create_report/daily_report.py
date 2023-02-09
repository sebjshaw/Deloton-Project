import base64
from datetime import datetime
from PGConnection import SQLConnection as postgres
import os
import math
from typing import Union 
import s3fs
import plotly.express as px
import boto3
from botocore.exceptions import ClientError
from visualisations import create_line_graph, create_grouped_bar_graph
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

pg = postgres(USERNAME, PASSWORD, HOST, PORT, DB_NAME)

def pull_txt_file_from_s3() -> str:
    """Pulls the txt file from the bucket that contains the number of hr warning emails that were sent in the last 24 hours

    Returns:
        str: the number of emails as a string
    """
    s3 = s3fs.S3FileSystem(anon=False)
    file = s3.find('three-m-deloton-bucket/hr_emails.txt')

    with s3.open(file[0]) as f:
        total_emails = f.read()
        total_emails = total_emails.decode("utf-8")

    return total_emails


def get_total_daily_rides() -> px.line:
    """Creates a line graph tracking the total rides over the last 7 days 

    Returns:
        px.line: line graph creates by plotly.express
    """

    # count the number of rides grouped by day 
    df = pg.get_df("""
    SELECT 
        COUNT(ride_id) AS total_rides, 
        to_char(DATE(date), 'Dy') AS day
    FROM rides 
    WHERE DATE(date) > CURRENT_DATE - INTERVAL '7 days' 
    GROUP BY date 
    ORDER BY date ASC;""")


    return create_line_graph(df, 'day', 'total_rides')

def get_avg_ride_length_by_gender_and_age() -> px.bar:
    """Gets the average ride length split by user gender and age for last 24 hours. 
    Returns bar graph visualising the results

    Returns:
        px.bar: bar graph visualising the result of the query
    """
    df = pg.get_df(
		"""
			SELECT 
				u.gender,
				CASE
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) < '18 years' THEN '<18'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '18 years' AND '24 years' THEN '18-24'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '25 years' AND '34 years' THEN '25-34'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '35 years' AND '44 years' THEN '35-44'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '45 years' AND '54 years' THEN '45-54'
					WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '55 years' AND '64 years' THEN '55-64'
					ELSE '65+'
				END AS age_group,
				AVG(r.total_duration) AS average_duration
			FROM users u
				JOIN rides r
					USING(user_id)
			WHERE EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24
			GROUP BY age_group, gender
			ORDER BY age_group;
		"""
	)
    return create_grouped_bar_graph(df, 'age_group', 'average_duration', 'gender', 'Average Ride Duration', 's')


def get_avg_power_by_gender_and_age() -> px.bar:
    """Gets the average power length split by user gender and age for las 24 hours. 
    Returns bar graph visualising the results

    Returns:
        px.bar: bar graph visualising the result of the query
    """
    df = pg.get_df(
		f"""
				SELECT 
					u.gender,
					CASE
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) < '18 years' THEN '<18'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '18 years' AND '24 years' THEN '18-24'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '25 years' AND '34 years' THEN '25-34'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '35 years' AND '44 years' THEN '35-44'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '45 years' AND '54 years' THEN '45-54'
						WHEN AGE(TO_DATE(u.date_of_birth,'YYYY-MM-DD')) BETWEEN '55 years' AND '64 years' THEN '55-64'
						ELSE '65+'
					END AS age_group,
					AVG(r.average_power*r.total_duration) AS average_power
				FROM users u
					JOIN rides r
						USING(user_id)
				WHERE EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24
				GROUP BY gender, age_group
				ORDER BY age_group;
		"""
	)
    return create_grouped_bar_graph(df, 'age_group', 'average_power', 'gender', 'Average Power', 'W')

def get_avg_power() -> int:
    """Gets the average power per ride for the last 24 hours

    Returns:
        int: average power as an integer
    """
    value = pg.get_list(f"""
            SELECT 
                AVG(r.average_power*r.total_duration) AS average_power
            FROM rides AS r
            WHERE 
                EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24
            """)[-1][0]
    return value 

def get_total_ride_time(gender:str) -> int:
    """Gets the total ride time in the last 24 hours. Can be split by gender
    Args:
        gender (str): The gender which the function will calculate the total ride time for 
    Returns:
        int: total ride time as an integer
    """
    if gender == 'both':
        value = pg.get_list(f"""
                SELECT 
                    SUM(r.total_duration) AS total_ride_time
                FROM rides AS r
                WHERE 
                    EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24
                """)[-1][0]
    else:
        value = pg.get_list(f"""
                SELECT 
                    SUM(r.total_duration) AS total_ride_time
                FROM users u
					JOIN rides r
						USING(user_id)
                WHERE 
                    (EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24) AND (u.gender = '{gender}')
                """)[-1][0]
    return value

def get_avg_hr() -> int:
    """Gets the average heart rate per ride for the last 24 hours

    Returns:
        int: average heart rate as an integer
    """
    value = pg.get_list(f"""
            SELECT 
                AVG(r.average_heart_rate) AS average_hr
            FROM rides AS r
            WHERE 
                EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24
            """)[-1][0]
    return value 

def get_longest_ride() -> int:
    value = pg.get_list(f"""
            SELECT 
                total_duration
            FROM rides AS r
            WHERE 
                EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24
            ORDER BY 
                total_duration DESC
            LIMIT 1
            """)[-1][0]
    return value

def get_largest_power() -> int:
    value = pg.get_list(f"""
            SELECT 
                max_power
            FROM rides AS r
            WHERE 
                EXTRACT(EPOCH FROM AGE(NOW(), CAST(CONCAT(r.date, ' ',r.time_started) as TIMESTAMP)))/3600 < 24
            ORDER BY 
                max_power DESC
            LIMIT 1
            """)[-1][0]
    return value
    
def encode_logo_as_base64() -> str:
    """Takes the logo png and encodes as base64 for insertion into the html template

    Returns:
        str: base64 encoded logo.png
    """

    with open("deleton_logo.png", "rb") as image_file:
        encoded_string = str(base64.b64encode(image_file.read()))[2:-1]

    logo_html = (f'<img class="figure" src="data:image/png;base64,{encoded_string}"><br>')

    return logo_html

def figure_to_base64(figure: Union[px.bar, px.line]) -> str:
    """Takes a plotly graph and encodes a png version as base64 to be inserted into the html template

    Args:
        figure (px.plot): either a plotly bar or line chart  

    Returns:
        str: base64 encoded png version of the plotly graph
    """

    image = str(base64.b64encode(figure.to_image(format="png", scale=2)))[2:-1]
    image_html = (f'<img class="figure" src="data:image/png;base64,{image}"><br>')
 
    return image_html

def create_html_report(template_file: str, content_dict: dict) -> str:
    """Creates the html report from the template and the dictionary of content 

    Args:
        template_file (str): template html file name
        content_dict (dict): dictionary of content

    Returns:
        str: html template with variables replaced with relevant content
    """

    with open(template_file, 'r') as f:
        template_html = f.read()

    report_html = template_html
    for content in content_dict:
        report_html = report_html.replace(content, content_dict[content])
        

    return report_html
 
def push_html_to_s3(today: str):
    """Push html file to s3 bucket
    Args:
        today (str): today's date
    """
    
    s3_client = boto3.client('s3')
    s3_client.upload_file(f'{today}.html','three-m-deleton-report',f'{today}.html')

def send_ceo_report_email():
    """Receives the link to the index page containing links to current and past daily reports and sends an email 
    to the CEO using SES 
    """

    SENDER = "trainee.alex.skowronski@sigmalabs.co.uk"
    # RECIPIENT = "bicycle-ceo@sigmalabs.co.uk"
    RECIPIENT = "trainee.seb.shaw@sigmalabs.co.uk"

    AWS_REGION = "eu-west-2"

    """The subject line for the email."""
    SUBJECT = "Deleton Daily Report"

    """The email body for recipients with non-HTML email clients."""
    BODY_TEXT = ("")
                
    """The HTML body of the email."""
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h2>Daily Report</h2>
    
    <h4>Dear CEO,</h4>
    <h4>We hope this finds you well. This email contains a link to the back log of daily reports. 
    The most recent report will be at the top.</h4>

    <a href="https://three-m-deleton-report.s3.eu-west-2.amazonaws.com/index.html">Daily Reports</a>
     
    <h5>This email was sent to you by The Three Musketeers.</h5>
    </body>
    </html>
                """            

    CHARSET = "UTF-8"

    """Create a new SES resource and specify a region."""
    client = boto3.client('ses',region_name=AWS_REGION)

    """Try to send the email."""
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
        
                        'Data': BODY_HTML
                    },
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event,context):
    today = str(datetime.now().date())
    total_rides = get_total_daily_rides()
    total_rides_html = figure_to_base64(total_rides)
    avg_power = f"{(round(get_avg_power(), 2))} W"
    total_ride_time = f"{get_total_ride_time('both')} s"
    ride_time_m = f"{get_total_ride_time('Male')} s"
    ride_time_f = f"{get_total_ride_time('Female')} s"
    avg_hr = f"{math.floor(get_avg_hr())} bpm"
    avg_ride_dur = get_avg_ride_length_by_gender_and_age()
    avg_ride_dur_html = figure_to_base64(avg_ride_dur)
    avg_ride_pow = get_avg_power_by_gender_and_age()
    avg_ride_pow_html = figure_to_base64(avg_ride_pow)
    over_max_hr = pull_txt_file_from_s3()
    max_power = f"{round(get_largest_power(), 2)} W"
    longest_ride = f"{get_longest_ride()} s"
    logo_html = encode_logo_as_base64()

    content_dict = {
        '{{ date }}':today,'{{ total_rides_graph }}':total_rides_html,
        '{{ avg_power }}':avg_power,'{{ total_ride_time }}':total_ride_time,
        '{{ ride_time_m }}': ride_time_m, '{{ ride_time_f }}': ride_time_f, '{{ avg_hr }}':avg_hr,
        '{{ avg_dur_graph }}':avg_ride_dur_html,'{{ avg_pow_graph }}':avg_ride_pow_html,
        '{{ over_max_hr }}':over_max_hr,'{{ max_power }}':max_power,
        '{{ longest_ride }}':longest_ride, '{{ logo }}': logo_html}

    report_html = create_html_report("template.html", content_dict)

    with open(f'{today}.html', 'w') as f:
        f.write(report_html)
    
    push_html_to_s3(today)

    send_ceo_report_email()

lambda_handler('x', 'x')


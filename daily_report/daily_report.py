import base64
from IPython.display import display, HTML
from xhtml2pdf import pisa
from datetime import datetime
from PGConnection import SQLConnection as postgres
import os
from visualisations import create_line_graph, create_grouped_bar_graph
from dotenv import load_dotenv
load_dotenv()


USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_NAME = os.getenv('DB_NAME')

pg = postgres(USERNAME, PASSWORD, HOST, PORT, DB_NAME)


def get_total_daily_rides():
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

def get_avg_ride_length_by_gender_and_age():
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
	return create_grouped_bar_graph(df, 'age_group', 'average_duration', 'gender', 'Average Ride Duration')

def figure_to_base64(figure):

    image = str(base64.b64encode(figure.to_image(format="png", scale=2)))[2:-1]
    image_html = (f'<img class="figure" src="data:image/png;base64,{image}"><br>')
 
    return image_html




today = str(datetime.now().date())
total_rides = get_total_daily_rides()
total_rides_html = figure_to_base64(total_rides)
item2 = 'Avg. Power'
item3 = 'Total Ride Time'
item4 = 'Total Rides M/F Split'
item5 = 'Avg. HR'
avg_ride_dur = get_avg_ride_length_by_gender_and_age()
avg_ride_dur_html = figure_to_base64(avg_ride_dur)
item7 = 'Avg. Ride resistance split by gender'
item8 = 'x riders went over max heart rate today'
item9 = 'x new riders today'
item10 = 'The Longest ride today'
logo = 'logo'
authors = 'authors'

content_dict = {
    '{{ date }}':today,'{{ item1 }}':total_rides_html,
    '{{ item2 }}':item2,'{{ item3 }}':item3,
    '{{ item4 }}':item4,'{{ item5 }}':item5,
    '{{ item6 }}':avg_ride_dur_html,'{{ item7 }}':item7,
    '{{ item8 }}':item8,'{{ item9 }}':item9,
    '{{ item10 }}':item10,}

def create_html_report(template_file, content_dict):
    with open(template_file, 'r') as f:
        template_html = f.read()

    report_html = template_html
    for content in content_dict:
        report_html = report_html.replace(content, content_dict[content])
        

    
    return report_html
 
 
report_html = create_html_report("template.html", content_dict)

with open('todays_report.html', 'w') as f:
    f.write(report_html)
 

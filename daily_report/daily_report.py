import base64
from IPython.display import display, HTML
from xhtml2pdf import pisa
from datetime import datetime
from PGConnection import SQLConnection as postgres
import os
import math
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
    """Gets the average ride length split by user gender and age for last 24 hours. 
    Returns bar graph visualising the results

    Returns:
        px.plot: bar graph visualising the result of the query
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

def get_avg_power_by_gender_and_age():
    """Gets the average power length split by user gender and age for las 24 hours. 
    Returns bar graph visualising the results

    Returns:
        px.plot: bar graph visualising the result of the query
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

def get_avg_power():
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

def get_total_ride_time(gender:str):
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

def get_avg_hr():
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

def get_longest_ride():
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

def figure_to_base64(figure):

    image = str(base64.b64encode(figure.to_image(format="png", scale=2)))[2:-1]
    image_html = (f'<img class="figure" src="data:image/png;base64,{image}"><br>')
 
    return image_html

today = str(datetime.now().date())
total_rides = get_total_daily_rides()
total_rides_html = figure_to_base64(total_rides)
avg_power = f"{(math.floor(get_avg_power()))} W"
total_ride_time = f"{get_total_ride_time('both')} s"
ride_time_m = f"{get_total_ride_time('Male')} s"
ride_time_f = f"{get_total_ride_time('Female')} s"
avg_hr = f"{math.floor(get_avg_hr())} bpm"
avg_ride_dur = get_avg_ride_length_by_gender_and_age()
avg_ride_dur_html = figure_to_base64(avg_ride_dur)
avg_ride_pow = get_avg_power_by_gender_and_age()
avg_ride_pow_html = figure_to_base64(avg_ride_pow)
over_max_hr = 'x riders went over max heart rate today'
new_riders = 'x new riders today'
longest_ride = f"{get_longest_ride()} s"
logo = 'logo'
authors = 'authors'

content_dict = {
    '{{ date }}':today,'{{ total_rides_graph }}':total_rides_html,
    '{{ avg_power }}':avg_power,'{{ total_ride_time }}':total_ride_time,
    '{{ ride_time_m }}': ride_time_m, '{{ ride_time_f }}': ride_time_f, '{{ avg_hr }}':avg_hr,
    '{{ avg_dur_graph }}':avg_ride_dur_html,'{{ avg_pow_graph }}':avg_ride_pow_html,
    '{{ over_max_hr }}':over_max_hr,'{{ new_riders }}':new_riders,
    '{{ longest_ride }}':longest_ride}

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
 

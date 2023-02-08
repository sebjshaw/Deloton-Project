from IPython.display import display, HTML
import base64
from datetime import datetime
from PGConnection import SQLConnection as postgres
import os
from xhtml2pdf import pisa
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
    ORDER BY date DESC;""")


    return create_line_graph(df, 'day', 'total_rides')

total_rides = get_total_daily_rides()


def figure_to_base64(figure):

    image = str(base64.b64encode(figure.to_image(format="png", scale=2)))[2:-1]
    images_html = (f'<img src="data:image/png;base64,{image}"><br>')
 
    return images_html

images_html = figure_to_base64(total_rides)

def create_html_report(template_file, images_html):
    with open(template_file, 'r') as f:
        template_html = f.read()
    
    report_html = template_html.replace("{{ FIGURES }}", images_html)
    
    return report_html
 
 
report_html = create_html_report("practice.html", images_html)

def convert_html_to_pdf(source_html, output_filename):
    with open(f"{output_filename}", "w+b") as f:
        pisa_status = pisa.CreatePDF(source_html, dest=f)
    
    print('PDF created')
    return pisa_status.err
 
 

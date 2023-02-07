
from jinja2 import FileSystemLoader, Environment
import pdfkit


date = "Today's Date"
item_1 = 'Total_Daily_Rides_Graph'
item_2 = 'Avg. Power'
item_3 = 'Total Ride Time'
item_4 = 'Total Rides M/F Split'
item_5 = 'Avg. HR'
item_6 = 'Avg. Ride Duration split by gender'
item_7 = 'Avg. Ride resistance split by gender'
item_8 = 'x riders went over max heart rate today'
item_9 = 'x new riders today'
item_10 = 'The Longest ride today'
footer = 'footer'

context = {
    'date': date, 'item_1': item_1, 'item_2': item_2, 'item_3': item_3,
    'item_4': item_4, 'item_5': item_5, 'item_6': item_6, 'item_7': item_7, 
    'item_8': item_8, 'item_9': item_9, 'item_10': item_10, 'footer':footer
    }


def load_html_template() -> str:
    """Loads the html template from file, adds the graphs and metrics and returns as string

    Returns:
        str: the daily_report formatted as a str
    """

    # create a template loader and template environment using jinja2
    template_loader = FileSystemLoader("./")
    template_env = Environment(loader=template_loader)

    # load in the html template, add the graphs and metrics and save as text
    template = template_env.get_template('index.html')
    return template.render(context)


def create_pdf_output(report_str:str):
    """Creates a pdf output of the daily report in the working directory 

    Args:
        report_str (str): the daily report in string format
    """

    # load text into pdf using pdfkit and wkhtmltopdf and the style.css file as styling
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    pdfkit.from_string(report_str, 'pdf_generated.pdf', configuration=config, css='style.css')




output_text = load_html_template()

create_pdf_output(output_text)



import jinja2
from jinja2 import Template
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


template_loader = jinja2.FileSystemLoader("./")
template_env = jinja2.Environment(loader=template_loader)

template = template_env.get_template('index.html')
output_text = template.render(context)



config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
pdfkit.from_string(output_text, 'pdf_generated.pdf', configuration=config, css='style.css')





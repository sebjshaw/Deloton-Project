from datetime import datetime
import math
import json
from botocore.exceptions import ClientError
import boto3

TODAY = datetime.now()

def calculate_max_heart_rate(dob: str):
    """Takes the date of birth of the user and returns the max heart rate

    Args:
        dob (str): The date of birth of the user in string format e.g. '1960-05-13'
    """

    dob = datetime(int(dob[:4]), int(dob[5:7]), int(dob[-2:]))
    age = math.floor(int(str(TODAY-dob).split(" ")[0])/365)

    return 220 - age #the max heart of the user is 220 - age

def compare_hr_to_max_hr(hr: str, max_hr: int) -> bool:
    """Return True if heart rate is above max, return False otherwise

    Args:
        hr (str): the current heart rate of the rider 
        max_hr (int): the max heart rate of the current rider

    Returns:
        bool: returns True (above max hr) or False (not above max hr)
    """

    if int(hr) >= max_hr:
        return True
    
    return False

def create_JSON_for_email(user_info: dict, curr_hr: int, max_hr:int, date: str, time_elapsed: str):

    new_user_info = {}
    new_user_info['user_forename'] = user_info['name'].split(" ")[0]
    new_user_info['user_surname'] = user_info['name'].split(" ")[1]
    new_user_info['curr_heart_rate'] = curr_hr
    new_user_info['limit_heart_rate'] = max_hr
    new_user_info['ride_date'] = date
    new_user_info['time_elapsed'] = time_elapsed
    new_user_info['user_email'] = user_info['email_address']

    send_user_hr_warning(new_user_info)

def send_user_hr_warning(user_info: dict, curr_hr: int, max_hr: int, date: str, time_elapsed: str):

    user_json = create_JSON_for_email(user_info, curr_hr, max_hr, date, time_elapsed)

    SENDER = "trainee.alex.skowronski@sigmalabs.co.uk"
    RECIPIENT = "three.musketeers.deloton@gmail.com"

    AWS_REGION = "eu-west-2"

    """The subject line for the email."""
    SUBJECT = "Heart Rate exceeding normal levels"

    """The email body for recipients with non-HTML email clients."""
    BODY_TEXT = ("You should be aware that your heart rate is exceeding the normal level of {}\r\n"
                "This email was sent to you by Deloton."
                )
                
    """The HTML body of the email."""
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>Hey {user_json["user_forename"]} {user_json["user_surname"]}, </h1>
    
    <h1>This email is to let you know that on {user_json["ride_date"]}, {user_json["time_elapsed"]} seconds into your ride
     your heart rate reached {user_json["curr_heart_rate"]} bpm, exceeding the typical limit of {user_json["limit_heart_rate"]} bpm.</h1>
     <h1>Stay safe!</h1>
     
    <h2>This email was sent to you by Deloton.</p>
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

# example email to send

# user_info = {
#     'date': '2023-02-02', 'time': '10:01:18.285918', 
#     'user_id': '4572', 'name': 'Harry Cook', 'gender': 'male', 
#     'address': 'Studio 69,Dickinson junction,East Timothy,L0 7EN', 
#     'date_of_birth': '1967-01-11', 'email_address': 'harry.c@gmail.com', 
#     'height_cm': '178', 'weight_kg': '66', 'account_create_date': '2022-02-21', 
#     'bike_serial': 'SN0000', 'original_source': 'social media'}

# curr_hr = 190
# max_hr = 187 # 33 years old
# date = '2023-02-02'
# duration = 24

# create_dict_for_email(user_info, curr_hr, max_hr, date, duration)

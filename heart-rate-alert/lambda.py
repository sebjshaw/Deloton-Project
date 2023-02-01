import boto3
from botocore.exceptions import ClientError
import datetime

def send_email(event):
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
    <h1>Hey {event["user_forename"]} {event["user_surname"]}, </h1>
    
    <h1>This email is to let you know that on {event["ride_date"]}, {event["time_elapsed"]} seconds into your ride
     your heart rate reached {event["curr_heart_rate"]} BPM, exceeding the typcial limit of {event["limit_heart_rate"]}.</h1>
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

def lambda_handler(event, context):
    # TODO implement
    send_email(event)

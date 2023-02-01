from datetime import datetime
import math

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

# initial plan was to send to lambda then the lambda can talk to the SNS but seems 
# that the EC2 can do this so will talk with the team in the morning 
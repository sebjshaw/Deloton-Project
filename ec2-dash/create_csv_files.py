import csv
import sqlite3

def most_recent_ride_to_csv(cursor: sqlite3.Cursor):
    """Writes the most recent ride to a csv file ready to be pushed to an s3 bucket

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
    """
    # retrieving all the data from the sqlite table
    cursor.execute("""
    SELECT * FROM current_ride
    """)
    most_recent_ride = cursor.fetchall()

    # writes the data to a csv file 
    with open("ec2-dash/most_recent_ride.csv", "w") as f:
        csv_f = csv.writer(f)
        csv_f.writerow(['user_id', 'ride_id', 'date', 'time', 'duration', 'resistance', 'heart_rate', 'rpm', 'power'])
        csv_f.writerows(most_recent_ride)

def user_info_to_csv(cursor: dict):
    """Writes the user information to a csv file ready to be pushed to an s3 bucket

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
    """
    # retrieving all the data from the sqlite table. If no SQLite table (i.e. consumer started halfway through a ride)
    # the user_info is N/A)
    try:
        cursor.execute("""
        SELECT * FROM user_info
        """)
        user_info = cursor.fetchall()
    except:
        user_info = [
            ('N/A','N/A','N/A',
            'N/A','N/A',
            'N/A','N/A',
            'N/A','N/A',
            'N/A','N/A')
            ]

    # writes the data to a csv file 
    with open("ec2-dash/user_info.csv", "w") as f:
        csv_f = csv.writer(f)
        csv_f.writerow(
            ['user_id', 'name', 'gender', 
            'address', 'date_of_birth', 
            'email_address', 'height_cm', 
            'weight_kg', 'account_create_date', 
            'bike_serial', 'original_source']
        )
        csv_f.writerows(user_info)
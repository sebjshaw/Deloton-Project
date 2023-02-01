import sqlite3
from kafka_consumer import create_kafka_consumer, create_log_entry
import csv
import boto3
import os

# create a boto3 client for when the csv needs to be uplaoded to the s3 bucket
s3 = boto3.client('s3')

# import the confluent kafka consumer 
c = create_kafka_consumer()

conn = sqlite3.connect('./ec2-dash/dash_db.db') #create an sqlite database and establish a connection

cursor = conn.cursor() #create a cursor to allow querying of the database

def create_new_current_ride_table(cursor: sqlite3.Cursor, conn: sqlite3.Connection):
    """Drops the previous table called current_ride and creates a new one. This function will be 
    called immediately after a new user information dict is received

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
        conn (sqlite3.Connection): Enables the query to be committed

    """

    
    cursor.execute("DROP TABLE IF EXISTS current_ride") #deletes the old current_ride table

    # creates a new current_ride table 
    cursor.execute("""
    CREATE TABLE current_ride (
        date TEXT, 
        time TEXT,
        duration INTEGER NOT NULL,
        resistance INTEGER NOT NULL, 
        heart_rate INTEGER NOT NULL,
        rpm INTEGER NOT NULL, 
        power TEXT NOT NULL
    )
    """)

    conn.commit()

def add_entry_to_table(cursor: sqlite3.Cursor,conn: sqlite3.Connection, entry: dict):
    """Adds an entry to the current_ride table. Called every time a new log is received 
    from the kafka consumer

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
        conn (sqlite3.Connection): Enables the query to be committed
        entry (dict): The combined log entry for this event
    """

    # query sent to the table current_ride to insert into table 
    cursor.execute(f"""
    INSERT INTO current_ride (
        date, time, duration, resistance, heart_rate, rpm, power
    )
    VALUES (
        "{entry['date']}", "{entry['time']}", 
        {entry['duration']}, {entry['resistance']}, 
        {entry['heart_rate']}, {entry['rpm']}, 
        "{entry['power']}"
    )
    """)

    conn.commit()

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
        csv_f.writerow(['ride_id', 'date', 'time', 'duration', 'resistance', 'heart_rate', 'rpm', 'power'])
        csv_f.writerows(most_recent_ride)

def create_user_info_table(cursor: sqlite3.Cursor, conn: sqlite3.Connection, user_info: dict):

    """Deletes previous user table, creates a new one and inserts the user information

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
        conn (sqlite3.Connection): Enables the query to be committed
        user_info (dict): The whole user information for the upcoming ride
    """

    cursor.execute("DROP TABLE IF EXISTS user_info") #deletes the old user_info table

    # creates a new user_info table and inserts the user information into it
    cursor.execute(f"""
    CREATE TABLE user_info (
        user_id INTEGER PRIMARY KEY, 
        name TEXT,
        gender TEXT NOT NULL,
        address TEXT NOT NULL, 
        date_of_birth TEXT NOT NULL,
        email_address TEXT NOT NULL, 
        height_cm INTEGER NOT NULL,
        weight_kg INTEGER NOT NULL,
        account_create_date TEXT NOT NULL,
        bike_serial TEXT,
        original_source TEXT
    );

    INSERT INTO user_info (
        user_id, name, gender, 
        address, date_of_birth, 
        email_address, height_cm, 
        weight_kg, account_create_date, 
        bike_serial, original_source
    )
    VALUES ({user_info['user_id']}, "{user_info['name']}", "{user_info['gender']}", 
    "{user_info['address']}", "{user_info['date_of_birth']}", 
    "{user_info['email_address']}", {user_info['height_cm']},
    {user_info['weight_kg']}, "{user_info['account_create_date']}",
    "{user_info['bike_serial']}", "{user_info['original_source']}"
    )
    """)

    conn.commit()

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

def push_to_s3():
    """Push both the log csv file and the user info csv file to the s3 bucket
    """

    s3.upload_file('ec2-dash/most_recent_ride.csv', 'three-m-deloton-bucket', 'most_recent_ride')
    s3.upload_file('ec2-dash/user_info.csv', 'three-m-deloton-bucket', 'user_info')

if __name__ == "__main__":
    create_new_current_ride_table(cursor, conn) #creates a table for the current ride data to be inserted into 

    # constantly retrieving logs and creating tables and csvs
    while True:
        try: 
            log_entry = create_log_entry(c)
            print(log_entry) #for reference, helps with debugging 
            
            # creates csv and pushes to s3, then deletes old current_ride table and creates new one 
            if log_entry.get('user_id') is not None:
                most_recent_ride_to_csv(cursor)
                user_info_to_csv(cursor)
                push_to_s3()
                create_new_current_ride_table(cursor, conn)
                os.remove("ec2-dash/most_recent_ride.csv") # delete the old log csv
                try:
                    os.remove("ec2-dash/user_info.csv") # delete the old user csv
                    create_user_info_table(cursor, conn, log_entry)
                except:
                    create_user_info_table(cursor, conn, log_entry)
                

            # only adds to the database if it is a full entry      
            if len(log_entry) == 7:
                add_entry_to_table(cursor, conn, log_entry)

        except KeyboardInterrupt:
            pass


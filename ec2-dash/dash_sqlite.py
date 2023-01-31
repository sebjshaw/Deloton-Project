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
        c (sqlite3.Cursor): The cursor that allows queries to be made to the database
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
    """Deletes the previous table called current_ride and creates a new. This function will be 
    called immediately after a new user information dict is received

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
        conn (sqlite3.Connection): Enables the query to be committed
        entry (dict): The combined log entry for this second
    """

    # insert into query sent to the table current_ride
    cursor.execute(f"""
    INSERT INTO current_ride (
        date, time, duration, resistance, heart_rate, rpm, power
    )
    VALUES (
        "{entry['date']}", "{entry['time']}", {entry['duration']}, {entry['resistance']}, {entry['heart_rate']}, {entry['rpm']}, "{entry['power']}"
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

    # delete the old csv 
    os.remove("ec2-dash/most_recent_ride.csv")

    # writes the data to a csv file 
    with open("ec2-dash/most_recent_ride.csv", "w") as f:
        csv_f = csv.writer(f)
        csv_f.writerow(['date', 'time', 'duration', 'resistance', 'heart_rate', 'rpm', 'power'])
        csv_f.writerows(most_recent_ride)

def push_to_s3():

    s3.upload_file('most_recent_ride.csv', bucket, most_recent_ride)

create_new_current_ride_table(cursor, conn) #creates a table for the current ride data to be inserted into 

while True:
    try: 
        log_entry = create_log_entry(c)
        print(log_entry)
        
        # creates csv and pushes to s3, then deletes old current_ride table and creates new one 
        if log_entry.get('user_id') is not None:
            most_recent_ride_to_csv(cursor)
            push_to_s3()
            create_new_current_ride_table(cursor, conn)

        # only adds to the database if it is a full entry      
        if len(log_entry) == 7:
            add_entry_to_table(cursor, conn, log_entry)
    except KeyboardInterrupt:
        pass


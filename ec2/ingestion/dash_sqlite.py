import sqlite3
from kafka_consumer import create_kafka_consumer, create_log_entry
from abnormal_hr import calculate_max_heart_rate, compare_hr_to_max_hr, create_dict_for_email, send_user_hr_warning
from create_csv_files import most_recent_ride_to_csv, user_info_to_csv
import boto3
import os
from datetime import datetime
import cache
import os
from dotenv import load_dotenv
load_dotenv


FEB_1_2023_SECS = datetime.strptime('2023-02-01 00:00:00', '%Y-%m-%d %H:%M:%S') #the first of Feb as a datetime object
NOW = datetime.now() #the second the program is initialised as a datetime object. For the ride_id of the interrupted ride

# create a boto3 client for when the csv needs to be uplaoded to the s3 bucket
s3 = boto3.client('s3')

# import the confluent kafka consumer 
c = create_kafka_consumer()

conn = sqlite3.connect('./ec2/ingestion/dash_db.db') #create an sqlite database and establish a connection

cursor = conn.cursor() #create a cursor to allow querying of the database

def recreate_ride_id_from_datetime(entry: dict) -> int:
    """Takes the first log entry and using the date and time creates a ride id as the number of seconds
    since the epoch

    Args:
        entry (dict): The log entry 

    Returns:
        int: returns the number of seconds since the epoch, to be used as ride_id
    """

    dt = entry['date'] + " " + entry['time'] #add the date and the time together
    dt = dt[:-7] #remove the decimals from the seconds
    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S') #convert to a datetime object

    ride_id = (dt - FEB_1_2023_SECS).total_seconds() #create a ride id (seconds since epoch)

    return ride_id

def recreate_current_ride_table(cursor: sqlite3.Cursor, conn: sqlite3.Connection):
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
        user_id TEXT,
        ride_id TEXT,
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

def add_entry_to_table(cursor: sqlite3.Cursor,conn: sqlite3.Connection, entry: dict, ride_id: int, user_id: str):
    """Adds an entry to the current_ride table. Called every time a new log is received 
    from the kafka consumer

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
        conn (sqlite3.Connection): Enables the query to be committed
        entry (dict): The combined log entry for this event
        ride_id (int): Adds the ride_id to each row of the table
        user_id (str): Adds the user_id to each row of the table 
    """

    # query sent to the table current_ride to insert into table 
    cursor.execute(f"""
    INSERT INTO current_ride (
        user_id, ride_id, date, time, duration, resistance, heart_rate, rpm, power
    )
    VALUES (
        "{user_id}", "{ride_id}", "{entry['date']}", 
        "{entry['time']}", {entry['duration']}, 
        {entry['resistance']}, {entry['heart_rate']}, 
        {entry['rpm']}, "{entry['power']}"
    )
    """)

    conn.commit()

def recreate_user_info_table(cursor: sqlite3.Cursor, conn: sqlite3.Connection, user_info: dict, max_hr: int):
    """Deletes previous user table, creates a new one and inserts the user information

    Args:
        cursor (sqlite3.Cursor): The cursor that allows queries to be made to the database
        conn (sqlite3.Connection): Enables the query to be committed
        user_info (dict): The whole user information for the upcoming ride
        max_hr (int): The max_hr is also included in the user info table
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
        original_source TEXT,
        max_hr INTEGER
    )
    """)
    conn.commit()

    cursor.execute(f"""
    INSERT INTO user_info (
        user_id, name, gender, 
        address, date_of_birth, 
        email_address, height_cm, 
        weight_kg, account_create_date, 
        bike_serial, original_source, max_hr
    )
    VALUES ({user_info['user_id']}, "{user_info['name']}", "{user_info['gender']}", 
    "{user_info['address']}", "{user_info['date_of_birth']}", 
    "{user_info['email_address']}", {user_info['height_cm']},
    {user_info['weight_kg']}, "{user_info['account_create_date']}",
    "{user_info['bike_serial']}", "{user_info['original_source']}", {max_hr}
    )
    """)

    conn.commit()

def push_csv_files_to_s3():
    """Push both the log csv file and the user info csv file to the s3 bucket
    """
    most_recent_ride_to_csv(cursor)
    user_info_to_csv(cursor)
    most_recent_ride_to_csv(cursor)
    user_info_to_csv(cursor)
    s3.upload_file('./ec2/ingestion/most_recent_ride.csv', 'three-m-deloton-bucket', 'most_recent_ride.csv')
    s3.upload_file('./ec2/ingestion/user_info.csv', 'three-m-deloton-bucket', 'user_info.csv')

def push_email_total_to_s3(total:int):
    with open('./ec2/ingestion/hr_emails.txt', 'w') as f:
        f.write(total)
    s3.upload_file('./ec2/ingestion/hr_emails.txt', 'three-m-deloton-bucket', 'hr_emails.txt')
    os.remove("./ec2/ingestion/hr_emails.txt")


if __name__ == "__main__":
    recreate_current_ride_table(cursor, conn) #creates a table for the current ride data to be inserted into 
    ride_id = str((NOW - FEB_1_2023_SECS).total_seconds())[:-6] #ride_id of interrupted ride is assigned now as start time 
    ride_date = 'N/A' #placeholder until user info is received
    max_hr = 220
    user_info = 'N/A' #placeholder until user info is received
    user_info = 'N/A' #placeholder until user info is received
    user_id = 0000
    total_hr_emails = 0
    
    # constantly retrieving logs and creating tables and csvs
    while True:
        try: 
            log_entry = create_log_entry(c)
            print(log_entry) #for reference, helps with debugging 
            try:
                if log_entry['time'][:-7] == "16:44:00":
                    push_email_total_to_s3(os.environ['TOTAL_HR_EMAILS'])
                    os.environ['TOTAL_HR_EMAILS'] = 0
            except:
                continue
            # creates csv and pushes to s3, then deletes old current_ride table and creates new one 
            if log_entry.get('user_id') is not None:
                push_csv_files_to_s3()
                push_csv_files_to_s3()
                
                # delete expired csv files 
                os.remove("./ec2/ingestion/most_recent_ride.csv") 
                os.remove("./ec2/ingestion/user_info.csv") 

                # set new max_hr
                max_hr = calculate_max_heart_rate(log_entry['date_of_birth'])

                #regenerate the tables
                recreate_current_ride_table(cursor, conn)
                recreate_user_info_table(cursor, conn, log_entry, max_hr)

                # regenerate the ride_id, user_id and ride_date
                ride_id = recreate_ride_id_from_datetime(log_entry)
                user_info = log_entry
                user_id = log_entry['user_id']
                ride_date = log_entry['date'] + " " + log_entry['time']
                
            # only adds to the database if it is a full entry      
            if len(log_entry) == 7:
                # adds entry to the table, user_id initially 0000 unless user_info has been received
                add_entry_to_table(cursor, conn, log_entry, ride_id, user_id)
                if compare_hr_to_max_hr(log_entry['heart_rate'], max_hr) == True and cache.check_cache_value(user_info['email_address']) is None:
                    cache.set_cache_value(user_info['email_address'])
                    user_email_dict = create_dict_for_email(user_info, int(log_entry['heart_rate']), max_hr, log_entry['date'], int(log_entry['duration'][:-2]))
                    send_user_hr_warning(user_email_dict)
                    os.environ['TOTAL_HR_EMAILS'] += 1
                    
        except KeyboardInterrupt:
            pass

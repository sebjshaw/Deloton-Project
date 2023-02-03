import pandas as pd
import os
import dotenv
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
import json
import boto3
import s3fs

dotenv.load_dotenv(override=True)

S3_BUCKET = os.getenv("S3_BUCKET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

RDS_ENDPOINT = os.environ['RDS_ENDPOINT']
RDS_PORT = os.environ['RDS_PORT']
RDS_USERNAME = os.environ['RDS_USERNAME']
RDS_PASSWORD = os.environ['RDS_PASSWORD']
RDS_DATABASE = os.environ['RDS_DATABASE']
RDS_SCHEMA_NAME = os.environ['RDS_SCHEMA_NAME']

def reorder_columns(dataframe, column_name, position_index):
    temp_column = dataframe[column_name]
    dataframe = dataframe.drop(columns = [column_name])
    dataframe.insert(loc = position_index, column = column_name, value = temp_column)

    return dataframe

def get_db_connection():
    conn = psycopg2.connect(
        host = f'{RDS_ENDPOINT}',
        dbname = f'{RDS_DATABASE}',
        user = f'{RDS_USERNAME}',
        password = f'{RDS_PASSWORD}',
        port = f'{RDS_PORT}'
    )
    return conn

def execute_query(query, conn):
    if conn!= None:
        with conn.cursor(cursor_factory= psycopg2.extras.RealDictCursor) as curs:
            curs.execute(query)
            conn.commit()
            return "Successfully applied query!"

def read_table(table_name, schema_name, connection):
    get_table = f"""
        SELECT * FROM {schema_name}.{table_name};
    """
    result = execute_query(get_table, connection)
    return result

def lambda_handler(event, context):

    """Loading in the user file from s3"""

    s3 = s3fs.S3FileSystem(anon=False)

    file = s3.find(f'{S3_BUCKET}/user_info')

    with s3.open(file[0]) as f:
        df = pd.read_csv(f, usecols = [0,1,2,3,4,5,6,7,8,9,10])

    # s3_client = boto3.client(
    #     "s3",
    #     aws_access_key_id = ACCESS_KEY,
    #     aws_secret_access_key = SECRET_KEY
    # )

    # response = s3_client.get_object(Bucket = S3_BUCKET, Key = "user_info", config=botocore.config.Config(s3={'addressing_style':'path'}))

    # status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    # if status == 200:
    #     print(f"Successful S3 get_object response. Status - {status}")
    #     df = pd.read_csv(response.get("Body"), usecols = [0,1,2,3,4,5,6,7,8,9,10])
    # else:
    #     print(f"Unsuccessful S3 get_object response. Status - {status}")

    # FILE_NAME = "user_info"
    # S3_BUCKET_URI = f"s3://{S3_BUCKET}/{FILE_NAME}"
    # # df = pd.read_csv(S3_BUCKET_URI, usecols = [0,1,2,3,4,5,6,7,8,9,10])

    """Transformation"""
    name_split = df['name'].str.split()

    first_name = name_split[0][-2]
    last_name = name_split[0][-1]

    df['first_name'] = first_name
    df['last_name'] = last_name
    #df[['first_name','last_name']] = df['name'].loc[df['name'].str.split().str.len() == 2].str.split(expand=True)

    df.drop(['name'], axis = 1, inplace = True)

    df['gender'] = list(map(lambda entry: entry.capitalize(), df['gender']))

    df = reorder_columns(df, 'first_name', 1)
    df = reorder_columns(df, 'last_name', 2)

    df.rename(columns = {
        "dob": "date_of_birth",
        "height": "height_cm",
        "weight": "weight_kg",
    }, inplace = True)

    df_users = df

    print(df_users)


    """Loading in the ride file from s3"""

    file = s3.find(f'{S3_BUCKET}/most_recent_ride')

    with s3.open(file[0]) as f:
        df = pd.read_csv(f)

    # # FILE_NAME = "most_recent_ride"
    # # S3_BUCKET_URI = f"s3://{S3_BUCKET}/{FILE_NAME}"
    # # df = pd.read_csv(S3_BUCKET_URI)

    # response = s3_client.get_object(Bucket = S3_BUCKET, Key = "most_recent_ride")

    # status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    # if status == 200:
    #     print(f"Successful S3 get_object response. Status - {status}")
    #     df = pd.read_csv(response.get("Body"))
    # else:
    #     print(f"Unsuccessful S3 get_object response. Status - {status}")

    """Accumulate metrics in a dictionary"""
    ride_metrics = {
        "user_id": 0,
        "ride_id": 0,
        "date": '2000-07-05',
        "time_started": '00:00:00.000000',
        "time_ended": '00:00:00.000000',
        "total_duration": 100.0,
        "max_resistance": 50,
        "max_heart_rate": 50,
        "max_rpm": 50,
        "max_power": 50.0,
        "average_resistance": 25,
        "average_heart_rate": 25,
        "average_rpm": 25,
        "average_power": 25,
    }

    ride_metrics["user_id"] = df["user_id"].iloc[0]
    ride_metrics["ride_id"] = df["ride_id"].iloc[0]
    ride_metrics["date"] = df["date"].iloc[0]
    ride_metrics["time_started"] = df["time"].iloc[0]
    ride_metrics["time_ended"] = df["time"].iloc[-1]
    ride_metrics["total_duration"] = df["duration"].iloc[-1]

    """Now calculate max values"""
    ride_metrics["max_resistance"], ride_metrics["max_heart_rate"],  = df["resistance"].max(), df["heart_rate"].max()
    ride_metrics["max_rpm"], ride_metrics["max_power"],  = df["rpm"].max(), df["power"].max()

    """Now calculate average values"""
    ride_metrics["average_resistance"], ride_metrics["average_heart_rate"],  = df["resistance"].mean(), df["heart_rate"].mean()
    ride_metrics["average_rpm"], ride_metrics["average_power"],  = df["rpm"].mean(), df["power"].mean()

    df_rides = pd.DataFrame([ride_metrics])

    print(df_rides)

    conn = get_db_connection()

    execute_query("""
        CREATE TABLE IF NOT EXISTS rides (
            user_id INT DEFAULT NULL,
            ride_id INT DEFAULT NULL,
            date VARCHAR(255) DEFAULT NULL,
            time_started VARCHAR(255) DEFAULT NULL,
            time_ended VARCHAR(255) DEFAULT NULL,
            total_duration DECIMAL DEFAULT NULL,
            max_resistance INT DEFAULT NULL,
            max_heart_rate INT DEFAULT NULL,
            max_rpm INT DEFAULT NULL,
            max_power DECIMAL DEFAULT NULL,
            average_resistance INT DEFAULT NULL,
            average_heart_rate INT DEFAULT NULL,
            average_rpm INT DEFAULT NULL,
            average_power DECIMAL DEFAULT NULL,
            PRIMARY KEY (user_id, ride_id)
        );
    """, conn)

    """Creating the users table"""
    execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT NULL,
            first_name VARCHAR(255) DEFAULT NULL,
            last_name VARCHAR(255) DEFAULT NULL,
            gender VARCHAR(255) DEFAULT NULL,
            address VARCHAR(255) DEFAULT NULL,
            date_of_birth VARCHAR(255) DEFAULT NULL,
            email_address VARCHAR(255) DEFAULT NULL,
            height_cm INT DEFAULT NULL,
            weight_kg INT DEFAULT NULL,
            account_create_date TIMESTAMP DEFAULT NULL,
            bike_serial VARCHAR(255) DEFAULT NULL,
            original_source VARCHAR(255) DEFAULT NULL,
            PRIMARY KEY (user_id)
        );
    """, conn)

    ENDPOINT = 'three-musketeers-warehouse.c1i5dspnearp.eu-west-2.rds.amazonaws.com'

    conn_string = f'postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{ENDPOINT}:{RDS_PORT}/postgres'

    db = create_engine(conn_string)

    conn = db.connect()

    df_users.to_sql('users', con = conn, if_exists = 'append', index = False)
    df_rides.to_sql('rides', con = conn, if_exists = 'append', index = False)

    conn = psycopg2.connect(conn_string)
    conn.autocommit = True

    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

event, context = {}, {}
lambda_handler(event, context)
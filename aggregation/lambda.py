import pandas as pd
import os
import dotenv
import json
from PGConnection import SQLConnection
import s3fs
import boto3

dotenv.load_dotenv()
HOST = os.environ['HOST']
PORT = os.environ['PORT']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
DB_NAME = os.environ['DB_NAME']

# Loading environment variables
S3_BUCKET = os.getenv("S3_BUCKET")

sql = SQLConnection(USERNAME,PASSWORD,HOST,PORT,DB_NAME)
s3 = boto3.client('s3')

table_cols = {
    'rides': [
        'user_id','ride_id','date','time_started','time_ended','total_duration',
        'max_resistance','max_heart_rate','max_rpm','max_power','average_resistance',
        'average_heart_rate','average_rpm','average_power'
    ],
    'users': [
        'user_id','first_name','last_name','gender','address','date_of_birth','email_address',
        'height_cm','weight_kg','account_create_date','bike_serial','original_source'
    ]
}          

def reorder_columns(df:pd.DataFrame, table_name:str) -> pd.DataFrame:
    """
    correct the order of the columns in the dataframe to match the
    PostgreSQL table

    Args:
        df (pd.DataFrame): df
        table_name (str): exact table name from Postgres

    Returns:
        pd.DataFrame: reordered df
    """
    df = df[table_cols[table_name]]
    return df

def create_rides_table_entry(file_name: str, user_id:str) -> pd.DataFrame:
    """
    Collect the file from S3 and create a dataframe
    row with the required metrics measured from the user's
    ride

    Args:
        file_name (str): name of the file in the s3 bucket
        user_id (str): user_id

    Returns:
        pd.DataFrame: dataframe containing aggregated data from the user's ride
    """

    s3.download_file(S3_BUCKET, file_name, f'./{file_name}')
    with open(f'./{file_name}') as file:
        df = pd.read_csv(file)
    os.remove(f'./{file_name}')

    #df = pd.read_csv(f's3://{S3_BUCKET}/{file_name}')

    # Accumulate metrics in a dictionary
    rides_object = {}
    rides_object["user_id"] = user_id
    rides_object["ride_id"] = df["ride_id"].iloc[0]
    rides_object["date"] = df["date"].iloc[0]
    rides_object["time_started"] = df["time"].iloc[0]
    rides_object["time_ended"] = df["time"].iloc[-1]
    rides_object["total_duration"] = df["duration"].iloc[-1]
    rides_object["max_resistance"] = df["resistance"].max()
    rides_object["max_heart_rate"] = df["heart_rate"].max()
    rides_object["max_rpm"] = df["rpm"].max()
    rides_object["max_power"] = df["power"].max()
    rides_object["average_resistance"] = df["resistance"].mean()
    rides_object["average_heart_rate"] = df["heart_rate"].mean()
    rides_object["average_rpm"] = df["rpm"].mean()
    rides_object["average_power"] = df["power"].mean()

    df_rides = pd.DataFrame([rides_object])
    return df_rides

def create_users_table_entry(file_name:str) -> pd.DataFrame:
    """
    Collect the file from S3 and create a dataframe
    row with users info

    Args:
        file_name (str): name of the file in the s3 bucket

    Returns:
        pd.DataFrame: dataframe containing user's data
    """

    s3.download_file(S3_BUCKET, file_name, f'./{file_name}')
    with open(f'./{file_name}') as file:
        df = pd.read_csv(file)
    os.remove(f'./{file_name}')
    
    #df = pd.read_csv(f's3://{S3_BUCKET}/{file_name}')

    # Transformation
    name_split = df['name'].str.split()
    first_name = name_split[0][-2]
    last_name = name_split[0][-1]
    df['first_name'] = first_name
    df['last_name'] = last_name
    df.drop(['name'], axis = 1, inplace = True)
    df['gender'] = list(map(lambda entry: entry.capitalize(), df['gender']))

    df = reorder_columns(df, 'users')

    df.rename(columns = {
        "dob": "date_of_birth",
        "height": "height_cm",
        "weight": "weight_kg",
    }, inplace = True)

    return df

def lambda_handler(event, context):
    df_users = create_users_table_entry('user_info.csv')
    user_id = df_users.user_id.iloc[0]
    df_rides = create_rides_table_entry('most_recent_ride.csv', user_id)
    sql.get_list(
        """
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
        """
    )

    sql.get_list(
        """
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
        """
    )
    try:
        df_users.to_sql('users', con = sql.engine, if_exists = 'append', index = False)
        print(f'user id {df_users.user_id.iloc[0]} added')
    except:
        print("user already exists")

    try:
        df_rides.to_sql('rides', con = sql.engine, if_exists = 'append', index = False)
        print(f'ride id {df_rides.ride_id.iloc[0]} for user id {df_rides.user_id.iloc[0]} added')
    except:
        print('ride already in database')

    

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

lambda_handler({},{})
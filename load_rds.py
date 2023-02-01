import psycopg2
import psycopg2.extras
import os
import dotenv
import json

dotenv.load_dotenv(override=True)

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# s3 = boto3.client("s3")
# S3_BUCKET_NAME = "three-m-deloton-bucket"
# S3_OBJECT_NAME = "test_ride.csv"

RDS_ENDPOINT = 'three-musketeers-warehouse.c1i5dspnearp.eu-west-2.rds.amazonaws.com'
RDS_PORT = 5432
RDS_USERNAME = 'three_musk'
RDS_PASSWORD = 'password'
RDS_DATABASE = 'postgres'
RDS_SCHEMA_NAME = 'public'

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
            return
            returned_data = curs.fetchall()
            return returned_data

def read_table(table_name, schema_name, connection):
    get_table = f"""
        SELECT * FROM {schema_name}.{table_name};
    """
    #result = execute_query(get_table, connection)
    execute_query(get_table, connection)
    return sqlio.read_sql_query(get_table, connection)

def lambda_handler(event, context):

    conn = get_db_connection()

    """Creating the rides table"""
    execute_query("""
        CREATE TABLE IF NOT EXISTS rides (
            ride_id INT DEFAULT NULL,
            date VARCHAR(255) DEFAULT NULL,
            time VARCHAR(255) DEFAULT NULL,
            duration DECIMAL DEFAULT NULL,
            resistance INT DEFAULT NULL,
            heart_rate INT DEFAULT NULL,
            rpm INT DEFAULT NULL,
            power DECIMAL DEFAULT NULL,
            PRIMARY KEY (ride_id)
        );
    """, conn)

    """Creating the users table"""
    execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT NOT NULL,
            name VARCHAR(255) DEFAULT NULL,
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

    """Create join table"""
    execute_query(f"""
        CREATE TABLE IF NOT EXISTS users_rides (
            ride_id INT NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (ride_id) REFERENCES rides (ride_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        );
    """, conn)


    """Populate rides table"""
    execute_query(f"""
        SELECT aws_s3.table_import_from_s3(
            'rides', 'date,time,duration,resistance,heart_rate,rpm,power', '(format csv, header true)',
            'three-m-deloton-bucket', '/most_recent_ride', 'eu-west-2',
            '{AWS_ACCESS_KEY_ID}', '{AWS_SECRET_ACCESS_KEY}'
        );
    """, conn)

    """Populate user table from user.csv"""
    execute_query(f"""
        SELECT aws_s3.table_import_from_s3(
            'users', 'user_id,name,gender,address,date_of_birth,email_address,height_cm,weight_kg,account_create_date,bike_serial,original_source', 
            '(format csv, header true)', 'three-m-deloton-bucket', '/user_info', 'eu-west-2',
            '{AWS_ACCESS_KEY_ID}', '{AWS_SECRET_ACCESS_KEY}'
        );
    """, conn)

    """Populate join table"""
    execute_query(f"""
        SELECT aws_s3.table_import_from_s3(
            'users_rides', 'user_id,ride_id',
            '(format csv, header true)', 'three-m-deloton-bucket', '/join_ids', 'eu-west-2',
            '{AWS_ACCESS_KEY_ID}', '{AWS_SECRET_ACCESS_KEY}'
        );
    """, conn)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# https://www.youtube.com/watch?v=l-v6FodULk0
# pandas to sql command but try above

event, context = {}, {}
lambda_handler(event, context)
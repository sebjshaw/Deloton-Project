import psycopg2
import pandas as pd
import sqlalchemy
import dotenv
import os

dotenv.load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv()
HOST = os.getenv()
PORT = os.getenv()
DB_NAME = os.getenv()

class SQLConnection():
	"""Create a SQLite connection class
	"""
	def __init__(self, database_file: str) -> None:
		self.engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
		self.conn = self.engine.connect()
	
	def get_df(self, query:str) -> pd.DataFrame:
		"""
		query the database

		Args:
			query (str): string used to query the database

		Returns:
			pd.DataFrame: result of the query
		"""
		try:
			res = pd.read_sql_query(query, self.conn)
			print(f"Querying: '{query}'")
			return res
		except Exception as e:
			print(e)
			print('\n')

	def get_list(self, query:str) -> list[tuple]:
		"""
		Execute a query on the db

		Args:
				query (str): query string

		Returns:
				list: returned from query
		"""
		query = sqlalchemy.text(query)
		try:
			res = self.conn.execute(query)
			res = res.fetchall()
			print(f"'{query}' executed")
			return res
		except Exception as e:
			print(e)
			print('\n')
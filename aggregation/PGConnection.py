import psycopg2
import pandas as pd
import sqlalchemy

class SQLConnection():
	"""Create a PostgreSQL connection class
	NOTE: get_list can also be used to perform all other executions
	for a db, i.e. INSERT, DELETE, etc.
	"""
	def __init__(self, username:str, password:str, host:str, port:str, db_name:str) -> None:
		self.engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}')
		self.conn = self.engine.connect()
	
	def get_df(self, query:str) -> pd.DataFrame | None:
		"""
		query the database

		Args:
			query (str): string used to query the database

		Returns:
			pd.DataFrame: result of the query
		"""
		query = sqlalchemy.text(query)
		try:
			res = pd.read_sql_query(query, self.conn)
			print(f"Querying: '{query}'")
			return res
		except Exception as e:
			print(e)
			print('\n')

	def get_list(self, query:str) -> list[tuple] | None:
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
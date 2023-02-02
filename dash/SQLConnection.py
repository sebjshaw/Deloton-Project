import sqlite3
import pandas as pd

class SQLConnection():
	"""Create a SQLite connection class
	"""
	def __init__(self, database_file: str) -> pd.DataFrame | None:
		self.conn = sqlite3.connect(f'{database_file}')
		self.curs = self.conn.cursor()
	
	def query(self, query:str) -> pd.DataFrame:
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
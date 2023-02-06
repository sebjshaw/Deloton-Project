import sqlite3
import pandas as pd
import threading

lock = threading.Lock()

class SQLConnection():
	"""Create a SQLite connection class
	"""
	def __init__(self, database_file: str) -> None:
		self.conn = sqlite3.connect(f'{database_file}', check_same_thread=False)
		self.curs = self.conn.cursor()
	
	def get_df(self, query:str) -> pd.DataFrame:
		"""
		query the database

		Args:
			query (str): string used to query the database

		Returns:
			pd.DataFrame: result of the query
		"""
		try:
			lock.acquire(True)
			res = pd.read_sql_query(query, self.conn)
			print(f"Querying: '{query}'")
			return res
		except Exception as e:
			print(e)
			print('\n')
		finally:
			lock.release()

	def get_list(self, query:str) -> list[tuple]:
		"""
		Execute a query on the db

		Args:
				query (str): query string

		Returns:
				list: returned from query
		"""
		try:
			lock.acquire(True)
			res = self.curs.execute(query)
			res = res.fetchall()
			print(f"'{query}' executed")
			return res
		except Exception as e:
			print(e)
			print('\n')
		finally:
			lock.release()
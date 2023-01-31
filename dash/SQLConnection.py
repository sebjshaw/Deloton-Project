import sqlalchemy
import pandas as pd

class SQLConnection():
	def __init__(self, username: str, password: str, host: str, port: str, database: str) -> None:
		self.engine = sqlalchemy.create_engine(f'sqlite://{username}:{password}@{host}:{port}/{database}')
		self.conn = self.engine.connect()
	
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

	def load_to_staging(self, df:pd.DataFrame, schema_name='week4_dominic_staging', table_name='staging_ecommerce', if_exists='replace') -> None:
		"""
		Load to sql database, creating a new table or appending to existing table

		Args:
			df (pd.DataFrame): df containing data for the sql table
			schema (str): DEFAULT: week4_dominic_staging, schema to create table in
			table_name (str): DEFAULT: staging_ecommerce, name given to created sql table
			if_exists (str): DEFAULT: replace, course of action if table exists already [append, replace, fail] 

		Returns:
			str: _description_
		"""
		try:
			df.to_sql(table_name, self.conn, schema=schema_name, if_exists=if_exists, index = False)
			if if_exists == 'append':
				print(f'Appended to table {table_name} successfully')
			elif if_exists == 'replace':
				print(f'Replaced table {table_name} successfully')
		except Exception as e:
			print(f"Error loading to table {table_name}")
			print(e)
		print()

	def load_to_production(self, df:pd.DataFrame, schema_name='week4_dominic_production', table_name='production_ecommerce', if_exists='replace') -> None:
		"""
		Load to sql database, creating a new table or appending to existing table

		Args:
			df (pd.DataFrame): df containing data for the sql table
			schema (str): schema to create table in
			table_name (str): name given to created sql table
			if_exists (str): DEFAULT: append, course of action if table exists already [append, replace, fail] 

		Returns:
			str: _description_
		"""
		try:
			df.to_sql(table_name, self.conn, schema=schema_name, if_exists=if_exists, index = False)
			if if_exists == 'append':
				print(f'Appended to table {table_name} successfully')
			elif if_exists == 'replace':
				print(f'Daily update complete')
		except Exception as e:
			print(e)
		print('\n')

	def execute(self, query:str) -> list:
		"""
		Execute a query on the db

		Args:
				query (str): query string

		Returns:
				list: returned from query
		"""
		query = sqlalchemy.text(query)
		try:
			res = self.conn.execute(query).fetchall()
			print(f"'{query}' executed")
			return res
		except Exception as e:
			print(e)
		print('\n')
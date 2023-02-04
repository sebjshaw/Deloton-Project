import redis

redisClient = redis.Redis(host='localhost', port=6379)
# redis hashes, on for contries and one for institutes

def check_cache_value(email: str) -> bool | None:
	"""
	Check cache for user_email

	Args:
			email (str): user email

	Returns:
			bool: True if email in cache
	"""
	if redisClient.get(email):
		return True

def set_cache_value(email: str) -> None:
	"""
	set cache value to contain user email

	Args:
			email (str): user email
	"""
	redisClient.set(email, 'True', ex=15)
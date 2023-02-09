import s3fs
from bs4 import BeautifulSoup as bs
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('aws_access_key_id')
secret = os.getenv('aws_secret_access_key')

s3 = s3fs.S3FileSystem(anon=False, key=key, secret=secret)
boto = boto3.resource('s3')
bucket = "three-m-deleton-report"

def lambda_handler(event, context):
	contents = s3.ls(bucket)
	contents = [page.split("/")[-1] for page in contents if '.html' in page and 'index.html' not in page]
	contents.sort(reverse=True)
	file = open("index.html", "r")
	html = file.read()

	soup = bs(html,"html.parser")
	list_container = soup.find('ul')
	list_container.contents = []

	for item in contents:
		list_element = soup.new_tag('li')
		anchor_element = soup.new_tag('a')
		anchor_element["href"] = f"https://{bucket}.s3.eu-west-2.amazonaws.com/{item}"
		anchor_element.string = item
		list_element.append(anchor_element)
		list_container.append(list_element)

	changes = soup.prettify("utf-8")

	with open("index.html", 'wb') as file:
		file.write(changes)

	s3_path = f"s3://{bucket}/index.html"

	# Define the local file path
	local_path = "index.html"

	# Upload the file
	s3.put(local_path, s3_path)
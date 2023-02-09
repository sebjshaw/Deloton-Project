import s3fs
from bs4 import BeautifulSoup as bs
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

#credentials
key = os.getenv('aws_access_key_id')
secret = os.getenv('aws_secret_access_key')
index_path = 'index.html'

#s3 connection
s3 = s3fs.S3FileSystem(anon=False, key=key, secret=secret)
s3_client = boto3.client('s3', aws_access_key_id=key, aws_secret_access_key=secret)
bucket = "three-m-deleton-report"

#lambda function
def lambda_handler(event, context):
	contents = s3.ls(bucket)
	contents = [page.split("/")[-1] for page in contents if '.html' in page and 'index.html' not in page]
	contents = [page.split(".")[0] for page in contents]
	print(contents)
	contents.sort(reverse=True)
	file = open(index_path, "r")
	html = file.read()

	soup = bs(html,"html.parser")
	list_container = soup.find('ul')
	list_container.contents = []

	for item in contents:
		list_element = soup.new_tag('li')
		anchor_element = soup.new_tag('a')
		anchor_element["href"] = f"https://{bucket}.s3.eu-west-2.amazonaws.com/{item}.html"
		anchor_element.string = item
		list_element.append(anchor_element)
		list_container.append(list_element)

	changes = soup.prettify("utf-8")
	
	os.chdir('../../tmp')

	with open(index_path, 'wb') as file:
		file.write(changes)
		
	print(anchor_element)

	s3_path = f"s3://three-m-deloton-bucket/index.html"

	# Upload the file
	s3_client.upload_file('index.html', 'three-m-deloton-bucket', 'index.html', ExtraArgs={'ACL': 'public-read'})

	print('DONE')
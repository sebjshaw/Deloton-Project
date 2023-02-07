aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
docker tag fa7e39bf5ceb 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
aws lambda update-function-configuration --function-name Three-M-API-get --environment Variables={IMAGE_URI=605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get}
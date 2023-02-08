aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
docker tag 0165fc02c123 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
aws lambda update-function-code --function-name Three-M-API-get --image-uri 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
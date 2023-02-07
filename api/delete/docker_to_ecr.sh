aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
docker tag d69b4af8cef4 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-delete
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-delete
aws lambda get-function-configuration --function-name Three-M-API-delete
aws lambda update-function-configuration --function-name Three-M-API-delete --image 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-delete
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
docker tag f64fc03e416c 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-delete
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-delete
aws lambda update-function-code --function-name Three-M-API-delete --image-uri 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-delete
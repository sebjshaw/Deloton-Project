aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
<<<<<<< Updated upstream
docker tag 0165fc02c123 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
=======
docker tag e8ac5229adc2 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
>>>>>>> Stashed changes
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
aws lambda update-function-code --function-name Three-M-API-get --image-uri 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:api-get
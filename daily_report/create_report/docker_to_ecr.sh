aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
docker tag create_report 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:create_report
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:create_report
aws lambda update-function-code --function-name Three-M-Create-Report --image-uri 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:create_report
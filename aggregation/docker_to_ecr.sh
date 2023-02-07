aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
docker tag 6e66cd4f4ff7 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:deleton_s3_to_postgres
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:deleton_s3_to_postgres
aws lambda get-function-configuration --function-name Three-M-aggregation
aws lambda update-function-configuration --function-name Three-M-aggregation --image 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:deleton_s3_to_postgres
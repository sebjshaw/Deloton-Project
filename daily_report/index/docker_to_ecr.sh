aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 605126261673.dkr.ecr.eu-west-2.amazonaws.com
docker tag 8a063cd97ddf 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:dr-index-page-build
docker push 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:dr-index-page-build
aws lambda update-function-code --function-name Three-M-report-index --image-uri 605126261673.dkr.ecr.eu-west-2.amazonaws.com/three-musketeers:dr-index-page-build
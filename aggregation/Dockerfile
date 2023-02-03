FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
COPY .env .

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY lambda.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda.lambda_handler" ]
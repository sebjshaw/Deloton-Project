FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY .env .
COPY lambda.py ${LAMBDA_TASK_ROOT}
COPY PGConnection.py .

ENV PYTHONUNBUFFERED True


CMD [ "lambda.lambda_handler" ]
FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY lambda.py ${LAMBDA_TASK_ROOT}
COPY index.html .
COPY .env .

ENV PYTHONUNBUFFERED True


CMD [ "lambda.lambda_handler" ]
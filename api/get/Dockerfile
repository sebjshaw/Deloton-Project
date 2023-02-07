FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY .env .
COPY api_get.py ${LAMBDA_TASK_ROOT}
COPY SQLConnection.py .

ENV PYTHONUNBUFFERED True


CMD [ "api_get.lambda_handler" ]
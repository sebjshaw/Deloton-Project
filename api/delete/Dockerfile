FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY .env .
COPY api_delete.py ${LAMBDA_TASK_ROOT}
COPY SQLConnection.py .

ENV PYTHONUNBUFFERED True


CMD [ "api_delete.lambda_handler" ]
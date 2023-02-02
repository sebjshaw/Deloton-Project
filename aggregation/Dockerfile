FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
COPY .env .

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main" ]
FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY .env .
COPY deleton_logo.png .
COPY daily_report.py .
COPY PGConnection.py .
COPY visualisations.py .
COPY template.html .

ENV PYTHONUNBUFFERED True

CMD [ "daily_report.lambda_handler" ]
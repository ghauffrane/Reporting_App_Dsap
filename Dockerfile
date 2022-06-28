FROM python:3.8

WORKDIR /Reporting_App_Dsap
COPY ./app1/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

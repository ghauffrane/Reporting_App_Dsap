FROM python:3.8

WORKDIR /Reporting_App/
COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
COPY . .
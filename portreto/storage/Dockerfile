FROM python:3
ENV PYTHONUNBUFFERED 1

#Set default environment variables
ENV STORAGE_ID=0
ENV EXTERNAL_URL='http://localhost:8000'

RUN mkdir /app
RUN mkdir /data
WORKDIR /app
COPY django/requirements.txt /app/
# For installing requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
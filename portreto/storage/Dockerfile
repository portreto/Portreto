FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
RUN mkdir /data
WORKDIR /app
COPY django/requirements.txt /app/
# For installing requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
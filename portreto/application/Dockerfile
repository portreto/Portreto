FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY app_service/requirements.txt /app/
# For installing requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


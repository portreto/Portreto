FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /web_app
WORKDIR /web_app
COPY django/requirements.txt /web_app/
# For installing requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


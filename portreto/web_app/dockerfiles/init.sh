#Initialization script for web-app container

#  source python virtual environment
 source ./web_app/venv/bin/activate
#  excecute django using virtual environment
 ./web_app/venv/bin/python ./web_app/manage.py runserver 0.0.0.0:8000
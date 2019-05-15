# link data
ln -s /data /app/data
# Run server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:80

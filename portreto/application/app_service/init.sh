# Run server
python manage.py makemigrations
python manage.py migrate
echo "=====================================================CREATING SUPERUSER"
echo    "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')"| python manage.py shell
python manage.py runserver 0.0.0.0:80

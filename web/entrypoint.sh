#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py crontab show
python manage.py crontab add
python manage.py crontab show
echo "$(env ; crontab -l)" | crontab - 
service cron start
exec "$@"
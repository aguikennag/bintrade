#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install --upgrade pip

pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

#python manage.py loaddata dump.json
#python manage.py loaddata country.json
#python manage.py loaddata plans.json


export DJANGO_SUPERUSER_EMAIL=admin1@bintrade.finance
export DJANGO_SUPERUSER_USERNAME=admin1
export DJANGO_SUPERUSER_PASSWORD=!gyuigad%4

#python manage.py createsuperuser --no-input


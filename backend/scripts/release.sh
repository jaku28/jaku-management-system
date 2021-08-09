#!/bin/bash
cd backend

python manage.py migrate --no-input

if [[ $ENVIRONMENT == "stage" ]]
then
	python manage.py collectstatic --no-input -i admin -i s3direct -i *node_mod1ules* -i *bower_components* -i debug_toolbar -i rest_framework
    python manage.py loaddata fixtures/initial-data
fi

# to restore prod database on stage
#heroku pg:backups restore $(heroku pg:backups public-url --app emesh-prod) DATABASE_URL --app emesh-stage

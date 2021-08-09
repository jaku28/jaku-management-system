cd backend/AppWeb
python manage.py migrate --no-input
python manage.py loaddata ../demo/demo.json

# if [[ $ENVIRONMENT == "test" ]]
# then
#   python manage.py loaddata ../demo/demo.json
# fi

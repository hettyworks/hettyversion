# hettyversion

## Setup

```
docker-compose up -d
pip3.4 install -r requirements.txt
python3.4 manage.py db upgrade
python3.4 manage.py load_songdata
python3.4 manage.py runserver
```

## Admin

Flask-Admin is available here

* <http://localhost:5000/admin/>

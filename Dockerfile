FROM tiangolo/uwsgi-nginx-flask:flask-python3.5

COPY requirements.txt /setup/requirements.txt
RUN pip install -r /setup/requirements.txt
COPY ./ /app

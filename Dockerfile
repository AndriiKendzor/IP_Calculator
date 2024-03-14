#Dockerfile
FROM python:3.9.17-bookworm

#Allow statements and log messages to immediately apper in the logs
ENV PYTHONUNBUFFERED true
#Copy local code to the container image.
ENV APP_HOME /back-end
WORKDIR $APP_HOME
Copy . ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
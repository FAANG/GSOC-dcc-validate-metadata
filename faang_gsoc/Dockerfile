#Tells Docker to use the official python 3 image from dockerhub as a base image
FROM python:3.9.7
# Sets an environmental variable that ensures output from python is sent straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1
# Sets the container's working directory to /app
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Copies all files from our local project into the container
COPY . .


RUN python manage.py makemigrations

RUN python manage.py migrate
# runs the pip install command for all packages listed in the requirements.txt file
CMD ["python","manage.py","runserver","0.0.0.0:8000"]

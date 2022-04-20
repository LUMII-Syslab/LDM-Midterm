FROM python:3-alpine

RUN pip install Flask-PyMongo
RUN pip install PyJWT
RUN pip install flask_uploads
RUN pip install flask-login
RUN pip install requests

COPY . /app
WORKDIR /app

# Expose the Flask port
EXPOSE 5000

CMD [ "python", "-u", "./server.py" ]


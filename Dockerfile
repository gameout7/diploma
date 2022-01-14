FROM python:3.8-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=index.py
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]


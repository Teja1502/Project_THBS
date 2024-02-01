FROM python:latest
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

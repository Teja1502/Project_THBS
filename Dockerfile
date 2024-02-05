FROM python:3.10.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8002
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8002" ]

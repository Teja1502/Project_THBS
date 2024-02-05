# FROM python:3.10.12
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# COPY . .
# EXPOSE 8002
# ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8002" ]

# Stage 1: Build Stage
FROM python:3.10.12 as builder
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Stage 2: Final Stage
FROM python:3.10.12
WORKDIR /app
COPY --from=builder /app /app
COPY . .
RUN python manage.py migrate

# Set the entrypoint
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]


FROM python:latest
WORKDIR /app

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Define the entry point for the container
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8002"]

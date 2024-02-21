# FROM python:3.10.12
# WORKDIR /app 
# COPY requirements.txt requirements.txt 
# RUN pip3 install -r requirements.txt 
# COPY . . 
# ENTRYPOINT ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

FROM python:3.10.12
WORKDIR /app 

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt 

# Copy the rest of the application code
COPY . . 

# Run migrations and create superuser
RUN python manage.py migrate && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python manage.py shell

# Set the entrypoint to start the Django development server
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]


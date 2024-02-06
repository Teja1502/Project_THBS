FROM python:3.10.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python","manage.py","runserver","0.0.0.0:8000" ]
# FROM python:3.10.12
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# COPY . .
# # EXPOSE 8000
# ENTRYPOINT ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8002"]
# has context menu

# Stage 1: Build Stage
# FROM python:3.10.12 as builder
# WORKDIR /app
# COPY requirements.txt requirements.txt
# RUN pip install --upgrade pip

# RUN pip3 install -r requirements.txt

# # Stage 2: Final Stage
# FROM python:3.10.12-slim
# WORKDIR /app
# COPY --from=builder /app /app
# COPY . .
# RUN pip install --upgrade pip
# RUN pip3 install -r requirements.txt
# # RUN pip3 install django
# # RUN pip3 install mysqlclient
# # RUN python manage.py migrate

# # Set the entrypoint
# ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8002" ]
# Use an official Python runtime as a parent image
# First stage: Builder
# FROM python:3.9 AS builder

# # Set the working directory in the container
# WORKDIR /app

# # Copy the requirements file into the container at /app
# COPY requirements.txt .

# # Install any needed packages specified in requirements.txt
# RUN pip install --upgrade pip && \
#     pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# # Second stage: Final
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the dependencies and application code from the builder stage
# COPY --from=builder /wheels /wheels
# COPY . .

# # Install any dependencies from the wheels directory
# RUN pip install --no-cache /wheels/*

# # Expose port 8002
# EXPOSE 8002

# # Define the command to run your application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]


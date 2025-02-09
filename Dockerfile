# Use an official Python runtime as the parent image.
FROM python:3.10-slim

# Install system dependencies required by OpenCV and others.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements.txt file into the container.
COPY requirements.txt ./

# Install the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container.
COPY . .

# Expose the port your Flask app will run on.
EXPOSE 80

# Set environment variables.
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Define the command to run your application.
CMD ["python", "app.py"]


# Define the command to run your application.
CMD ["python", "app.py"]



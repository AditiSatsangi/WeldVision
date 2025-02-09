# Use an official Python runtime as the parent image.
FROM python:3.10-slim

# Install system dependencies required by OpenCV (which requires libGL.so.1)
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements.txt file into the container at /app.
COPY requirements.txt ./

# Install the Python dependencies from requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container.
COPY . .

# Expose the port your Flask app will run on (port 80 in your case).
EXPOSE 80

# Set environment variables.
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Define the command to run your application.
CMD ["python", "app.py"]



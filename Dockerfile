# 1. Use an official Python runtime as the parent image.
FROM python:3.10-slim

# 2. Set the working directory inside the container.
WORKDIR /app

# 3. Copy the requirements.txt file into the container at /app.
COPY requirements.txt ./

# 4. Install the Python dependencies from requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container.
COPY . .

# 6. Expose the port your Flask app will run on (port 80 in your case).
EXPOSE 80

# 7. Set environment variables if needed.
# These are optional because your app.py already specifies the host and port.
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 8. Define the command to run your application.
CMD ["python", "app.py"]

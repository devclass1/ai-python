# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install all Python dependencies in a single RUN command to reduce image layers
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    flask \
    requests \
    pillow \
    azure-cognitiveservices-vision-computervision \
    openai

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]

# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 6066 available to the world outside this container
# EXPOSE 6066

# Copy the wait-for-it.sh script and make it executable
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# # Create a shell script that runs wait-for-it.sh and then faust
# # The wait-for-it.sh script is used to wait for the Kafka container to be ready
# RUN echo -e '#!/bin/sh\n./wait-for-it.sh kafka:9092 -- faust -A app worker -l info' > start.sh
# # Install dos2unix and convert the line endings of start.sh
# RUN apt-get update && apt-get install -y dos2unix && dos2unix start.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

# RUN chmod +x start.sh

# Run the start.sh script when the container launches
CMD ["./start.sh"]
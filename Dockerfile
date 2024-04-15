# Use an official Python runtime as a parent image
FROM python:3.13.0a6-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN echo 'export AWS_ACCESS_KEY_ID=VAL1' >> ~/.bashrc
RUN echo 'export AWS_SECRET_ACCESS_KEY=VAL2' >> ~/.bashrc

# Expose the port Waitress will run on
EXPOSE 5000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Run app.py using Waitress when the container launches
CMD ["python", "app.py"]
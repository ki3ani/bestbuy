# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=cleanstore.settings.production

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Make sure the entrypoint.sh script is copied and made executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint script to run on container start
ENTRYPOINT ["/entrypoint.sh"]

# CMD is now used in conjunction with the entrypoint script, so adjust accordingly if needed
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cleanstore.wsgi:application"]

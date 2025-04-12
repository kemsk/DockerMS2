FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the app code into the container
COPY . .

# Run the Django app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.myproject.wsgi:application"]

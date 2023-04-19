# Use the official Python 3.11.2 image as the base image
FROM python:3.11.2-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 for the Uvicorn server
EXPOSE 8000

# Start the Uvicorn server using the main.py file
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

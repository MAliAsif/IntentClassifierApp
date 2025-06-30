# Use an official lightweight Python image as base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list to the container
COPY requirements.txt /app/

# Install Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code and project files into the container
COPY . /app/

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app using Uvicorn; note: 'api.main' matches the folder and file path
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

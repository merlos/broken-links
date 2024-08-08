FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY link_checker.py .

# Set the entrypoint to the Python script
ENTRYPOINT ["python", "link_checker.py"]

# Use an appropriate base image, for example, Python 3.11
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the local files to the container
COPY app.py /app/
COPY helper.py /app/
COPY configuration.json /app/
COPY FirebaseAdminSDK.json /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask web application
CMD ["python", "app.py"]

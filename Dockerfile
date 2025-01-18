FROM python:3.10-slim

WORKDIR /app

# Copy  Python script to container
COPY stats.py /app/stats.py

EXPOSE 8080

# Set default environment variable for log file path
ENV LOG_PATH=/app/access.log

# Run the Python server
CMD ["python", "stats.py"]
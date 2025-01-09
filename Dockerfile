# Use Official Python 3.10
FROM python:3.10-slim

# Setup working directory
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

EXPOSE 8080
CMD ["python", "main.py"]
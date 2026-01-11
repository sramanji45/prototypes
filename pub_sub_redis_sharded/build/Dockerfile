FROM python:3.11-slim

WORKDIR /app

# Install dependencies (Poetry or Pip)
RUN pip install redis==7.0.1

# Copy your code from the 'src' folder on your host
# to the current WORKDIR (which is /app)
COPY src/ .

CMD ["python", "subscriber.py"]
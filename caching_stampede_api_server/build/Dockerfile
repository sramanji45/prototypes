FROM python:3.11-slim

WORKDIR /app

# Install dependencies (Poetry or Pip)
RUN pip install flask

# Copy your code from the 'src' folder on your host
# to the current WORKDIR (which is /app)
COPY src/ .

# Now app.py is located at /app/app.py
CMD ["python", "app.py"]
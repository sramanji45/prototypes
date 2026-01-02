FROM python:3.11-slim
RUN pip install kazoo
COPY master_failover.py /app/master_failover.py
WORKDIR /app
CMD ["python", "master_failover.py"]

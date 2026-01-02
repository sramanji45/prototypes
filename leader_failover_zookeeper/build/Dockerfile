FROM python:3.11-slim
RUN pip install kazoo
COPY leader_failover.py /app/leader_failover.py
WORKDIR /app
CMD ["python", "leader_failover.py"]

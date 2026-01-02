FROM python:3.11-slim
RUN pip install etcd3 protobuf==3.20.3
COPY leader_failover.py /app/leader_failover.py
WORKDIR /app
CMD ["python", "leader_failover.py"]

import os
import socket
import time
from kazoo.client import KazooClient, KazooState
from kazoo.exceptions import NodeExistsError

# 1. Connect to Zookeeper
ZK_HOSTS = os.environ.get('ZK_HOSTS', 'zookeeper:2181')
zk = KazooClient(hosts=ZK_HOSTS)
while True:
    try:
        zk.start(timeout=5)
        print("Connected to ZooKeeper!")
        break
    except Exception as e:
        print(f"ZooKeeper not ready yet:{e}. Retrying in 2s...")
        time.sleep(2)

def master_logic():
    print("I am the Master")
    while True:
        # Perform Master duties here
        time.sleep(5)

def run_election(event=None):
    try:
        # 2. Attempt to become Master
        hostname = socket.gethostname()
        print(f"Aspring to become master:{hostname}")
        zk.create("/master", hostname.encode('utf-8'), ephemeral=True)
        master_logic()
    except NodeExistsError:
        print("Master is elected already. Standing by...")
        # 3. Watch the master node
        if zk.exists("/master", watch=run_election):
            print("Watching Master...")

# 4. Handle connection loss to prevent Split Brain
def connection_listener(state):
    if state == KazooState.LOST:
        print("Disconnected! Stopping Master duties.")
        os._exit(1)

zk.add_listener(connection_listener)

if __name__ == "__main__":
    run_election()
    while True:
        time.sleep(1)
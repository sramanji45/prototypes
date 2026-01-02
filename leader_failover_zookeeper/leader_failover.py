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

def leader_logic(hostname):
    print(f"I am the Leader:{hostname}")
    while True:
        # Perform Leader duties here
        time.sleep(5)

def leader_election(event=None):
    hostname = socket.gethostname()
    try:
        # 2. Attempt to become Leader
        print(f"Aspring to become leader:{hostname}")
        zk.create("/leader", hostname.encode('utf-8'), ephemeral=True)
        leader_logic(hostname)
    except NodeExistsError:
        print(f"Leader is elected already. Standing by:{hostname}")
        # 3. Watch the leader node
        if zk.exists("/leader", watch=leader_election):
            print("Watching Leader...")

# 4. Handle connection loss to prevent Split Brain
def connection_listener(state):
    if state == KazooState.LOST:
        print("Disconnected! Stopping Leader duties.")
        os._exit(1)

zk.add_listener(connection_listener)

if __name__ == "__main__":
    leader_election()
    while True:
        time.sleep(1)
import os
import socket
import time
import etcd3

etcd = etcd3.client(host=os.getenv("ETCD_HOST", "localhost"), port=2379)

"""
etcd uses Raft algorithm and quorum to avoid split brain scenario.
If we run 3 etcd instances then 2 of them have to agree with any change
"""

def leader_election():
    lease = etcd.lease(5)
    try:
        hostname = socket.gethostname()
        is_leader = etcd.put_if_not_exists('/leader', hostname, lease)

        if is_leader:
            print(f"Iam the Leader:{hostname}")
            try:
                while True:
                    # If lease refresh fails, it means we lost connection to etcd or
                    # the lease was revoked/expired.
                    lease.refresh()
                    time.sleep(2)
            except Exception as e:
                print(f"Heartbeat failed: {e}. Stepping down...")
                # Go back to being a Follower or restart the election process.
        else:
            print(f"I am Follower:{hostname}")
            events_iterator, cancel = etcd.watch("/leader")
            for event in events_iterator:
                if isinstance(event, etcd3.events.DeleteEvent):
                    print("Leader is Down")
                    cancel()
                    leader_election()
    except Exception as ex:
        print(ex)

leader_election()
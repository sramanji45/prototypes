### Build the app and etcd
```aiignore
$docker compose build
[+] Building 1.8s (12/12) FINISHED                                                                                                                                   
 => [internal] load local bake definitions                                                                                                                      0.0s
 => => reading from stdin 555B                                                                                                                                  0.0s
 => [internal] load build definition from Dockerfile                                                                                                            0.0s
 => => transferring dockerfile: 198B                                                                                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                             1.6s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                                   0.0s
 => [internal] load .dockerignore                                                                                                                               0.0s
 => => transferring context: 2B                                                                                                                                 0.0s
 => [1/4] FROM docker.io/library/python:3.11-slim@sha256:aa9aac8eacc774817e2881238f52d983a5ea13d7f5a1dee479a1a1d466047951                                       0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:aa9aac8eacc774817e2881238f52d983a5ea13d7f5a1dee479a1a1d466047951                                       0.0s
 => [internal] load build context                                                                                                                               0.0s
 => => transferring context: 899B                                                                                                                               0.0s
 => CACHED [2/4] RUN pip install etcd3 protobuf==3.20.3                                                                                                         0.0s
 => [3/4] COPY leader_failover.py /app/leader_failover.py                                                                                                       0.0s
 => [4/4] WORKDIR /app                                                                                                                                          0.0s
 => exporting to image                                                                                                                                          0.1s
 => => exporting layers                                                                                                                                         0.0s
 => => exporting manifest sha256:c1fe796e250dcdd23541ae44b13c78e1b7804ee9f7e545dc6fd6d96cce93467d                                                               0.0s
 => => exporting config sha256:55fe90bedc4bd52f667ad354af1f4c4f17103a3db708801ef8d545775b298506                                                                 0.0s
 => => exporting attestation manifest sha256:43f9b3439489d6abc007166b1477f2cb08595bdc7e9c80a125cebdf11b39df07                                                   0.0s
 => => exporting manifest list sha256:a73035ea54f0b2f74cceaf1ba7f5deb45ab9de0a2b851348ae66db3fd246fdd9                                                          0.0s
 => => naming to docker.io/library/build-app:latest                                                                                                             0.0s
 => => unpacking to docker.io/library/build-app:latest                                                                                                          0.0s
 => resolving provenance for metadata file                                                                                                                      0.0s
[+] Building 1/1
 ✔ build-app  Built
```
### Run the app
```aiignore
$docker compose --verbose up -d
WARN[0000] Found orphan containers ([build-worker-1 build-worker-2 build-zookeeper-1 build-user-service-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] Running 4/4
 ✔ Network build_etcd-net  Created                                                                                                                              0.0s 
 ✔ Container build-etcd-1  Healthy                                                                                                                              5.7s 
 ✔ Container build-app-2   Started                                                                                                                              5.8s 
 ✔ Container build-app-1   Started 

$docker ps
CONTAINER ID   IMAGE                                 COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
083bfb9185ae   build-app                             "python leader_failo…"   37 seconds ago   Up 31 seconds                                                           build-app-1
b403fa688bed   build-app                             "python leader_failo…"   37 seconds ago   Up 31 seconds                                                           build-app-2
9a14e7b91950   gcr.io/etcd-development/etcd:v3.5.0   "/usr/local/bin/etcd"    37 seconds ago   Up 36 seconds (healthy)   0.0.0.0:2379->2379/tcp, [::]:2379->2379/tcp   build-etcd-1
ea2273cf68f8   zookeeper:3.8                         "/docker-entrypoint.…"   2 hours ago      Up 2 hours                0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp   build-zookeeper-1
```
### Who is the leader
```aiignore
$docker compose logs  -f
app-1  | Iam the Leader:083bfb9185ae
app-2  | I am Follower:b403fa688bed
```
### Fail Over
```aiignore
$docker stop 083bfb9185ae
083bfb9185ae

$docker ps
CONTAINER ID   IMAGE                                 COMMAND                  CREATED         STATUS                   PORTS                                         NAMES
b403fa688bed   build-app                             "python leader_failo…"   3 minutes ago   Up 3 minutes                                                           build-app-2
9a14e7b91950   gcr.io/etcd-development/etcd:v3.5.0   "/usr/local/bin/etcd"    3 minutes ago   Up 3 minutes (healthy)   0.0.0.0:2379->2379/tcp, [::]:2379->2379/tcp   build-etcd-1
ea2273cf68f8   zookeeper:3.8                         "/docker-entrypoint.…"   2 hours ago     Up 2 hours               0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp   build-zookeeper-1

$docker compose logs  -f
app-1 exited with code 137
app-2   | Leader is Down
app-2   | Iam the Leader:b403fa688bed
```
### How to check leader in etcd
```aiignore
$docker exec -it build-etcd-1 etcdctl get /leader
/leader
b403fa688bed
```
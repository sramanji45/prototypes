### Create all the containers
```aiignore
cd api-gw-apisix/build
docker compose --verbose up -d
```

### Check running status
Specifically check apisix and etcd logs and ensure no errors 
```aiignore
$docker compose logs -f etcd
etcd-1  | {"level":"info","ts":"2025-12-26T09:38:31.979Z","caller":"embed/serve.go:140","msg":"serving client traffic insecurely; this is strongly discouraged!","address":"[::]:2379"}
$docker compose logs -f apisix

$docker ps
CONTAINER ID   IMAGE                                 COMMAND                  CREATED          STATUS                    PORTS                                                                                      NAMES
e22f6e30650d   apache/apisix:3.2.0-debian            "/docker-entrypoint.…"   20 minutes ago   Up 20 minutes             0.0.0.0:9080->9080/tcp, [::]:9080->9080/tcp, 0.0.0.0:9180->9180/tcp, [::]:9180->9180/tcp   build-apisix-1
dc06a5794207   build-user-service                    "python login_servic…"   20 minutes ago   Up 20 minutes             0.0.0.0:5001->5001/tcp, [::]:5001->5001/tcp                                                build-user-service-1
160bb312c06f   build-order-service                   "python user_service…"   20 minutes ago   Up 20 minutes             0.0.0.0:5002->5002/tcp, [::]:5002->5002/tcp                                                build-order-service-1
c1d782280965   gcr.io/etcd-development/etcd:v3.5.0   "/usr/local/bin/etcd"    20 minutes ago   Up 20 minutes (healthy)   0.0.0.0:2379->2379/tcp, [::]:2379->2379/tcp                                                build-etcd-1
```

### Create API Gateway rules
```aiignore
$sh setup-rules.sh
```

### Test
Use postman and fire the below URLs with 'X-Api-Key': 'super-secret-key-123' header
```
http://localhost:5000/auth/login 
http://localhost:5000/users/2
```
Fire the same URLs in the Browser and see if browser is getting redirected to the login URL or not
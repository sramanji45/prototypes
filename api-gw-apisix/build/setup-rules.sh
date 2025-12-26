curl "http://127.0.0.1:9180/apisix/admin/routes/1" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-X PUT -d '
{
  "uri": "/auth/*",
  "name": "login-service-route",
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "login-service:5001": 1
    }
  }
}'
curl "http://127.0.0.1:9180/apisix/admin/routes/2" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-X PUT -d '
{
  "uri": "/users/*",
  "name": "user-service-route",
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "order-service:5001": 1
    }
  }
}'
curl "http://127.0.0.1:9180/apisix/admin/routes/3" \
-H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
-X PUT -d '
{
  "uri": "/orders/*",
  "name": "order-service-route",
  "upstream": {
    "type": "roundrobin",
    "nodes": {
      "order-service:5001": 1
    }
  }
}'
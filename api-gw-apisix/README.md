### Run Login Service
python login_service.py

### Run User Service
python user_service.py

### Run API Gateway
python api_gateway.py

### Test
Use postman and fire the below URLs with 'X-Api-Key': 'super-secret-key-123' header
```
http://localhost:5000/users/1
http://localhost:5000/users/2
```
Fire the same URLs in the Browser and see if browser is getting redirected to the login URL or not
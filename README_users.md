# PhishShield

## Packages for RESTful web app
```
pip install Flask Flask-SQLAlchemy Flask-HTTPAuth Flask-JWT-Extended
```

## Register a New User
```
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/register -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"username": "testuser", "email": "testuser@example.com", "password": "password123"}'
```

## Login an Existing User and Save the Token
```
$loginResponse = Invoke-RestMethod -Uri http://127.0.0.1:5000/api/login -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"username": "testuser", "password": "password123"}'
$authToken = $loginResponse.token
```

## Use the Token for Logout
```
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/logout -Method Post -Headers @{ "Authorization" = "Bearer $authToken" }
```

## List All Users (Admin Only)
Assuming the token you saved is for an admin user:
```
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/admin/users -Method Get -Headers @{ "Authorization" = "Bearer $authToken" }
```

## Delete a Specific User (Admin Only)
Assuming you have a user ID and the token saved is for an admin user:
```
$userId = 2 # Replace with the actual user ID
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/admin/user/$userId -Method Delete -Headers @{ "Authorization" = "Bearer $authToken" }
```

## Request Data Deletion
```
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/user/data-deletion -Method Post -Headers @{ "Authorization" = "Bearer $authToken" }
```

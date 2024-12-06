# PhishShield Usage Instructions

First, clone the repo:
```
git clone https://github.com/Somashekarbm/PhishShield.git
cd PhishShield
```

## Packages to be Installed
The necessary packages are listed in the file [req_web_app.txt](req_web_app.txt). Create a Python environment:
```
virtualenv .venv
```
Activate it:
```
.venv\Scripts\activate
```
(The above command is specific to Windows)

And install the packages using pip:
```
pip install -r req_web_app.txt
```

## Running the App
Start the server by running the command:
```
python flask_app/app.py
```
You can then open the website by entering the correct URL in your favourite web browser (`http://127.0.0.1:5000/`), or directly interact with the app's REST API by running the commands below (Note that these are PowerShell commands. If you are using another shell then change them to the equivalent commands in that shell language).

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

## Get Predictions
Example request to classify a URL with the ML model having model_id 0:
```
$body = @{
    url = "http://example.com"
    model_id = "0"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/classify" -Method POST -Body $body -ContentType "application/json"
$response
```

## Sample URLs
```
mp3raid.com/music/krizz_kaliko.html
bopsecrets.org/rexroth/cr/1.htm	
br-icloud.com.br
recipelink.com/msgbrd/board_14/2007/DEC/29094.html
```

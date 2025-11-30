import requests
import json

# First, register a test user
register_url = "http://localhost:8000/api/auth/register"
register_data = {
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User",
    "phone": "+1234567890",
    "lat": 28.6139,
    "lon": 77.2090,
    "region": "Delhi"
}

try:
    register_response = requests.post(register_url, json=register_data)
    if register_response.status_code == 200:
        register_result = register_response.json()
        token = register_result["access_token"]
        print("Registration successful, got token")
    else:
        print(f"Registration failed: {register_response.text}")
        # Try to login if user already exists
        login_url = "http://localhost:8000/api/auth/login"
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result["access_token"]
            print("Login successful, got token")
        else:
            print(f"Login also failed: {login_response.text}")
            exit(1)
except Exception as e:
    print(f"Error during registration/login: {e}")
    exit(1)

# Test the fertilizer recommendation API
url = "http://localhost:8000/api/soil-health/fertilizer-recommendation"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Test data
test_data = {
    "temperature": 25,
    "humidity": 60,
    "moisture": 40,
    "soil_type": "Loamy",
    "crop_type": "Maize",
    "nitrogen": 30,
    "potassium": 20,
    "phosphorous": 15
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(test_data))
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("API Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error connecting to API: {e}")

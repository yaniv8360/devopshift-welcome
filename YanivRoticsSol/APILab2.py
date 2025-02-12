#this solution dont working
import json
from time import sleep
import httpx

URL = "https://api.example.com/system/metrics"
our_data = {"metrics": "cpu,memory"}
headers = {"Authorization": "Bearer YOUR_API_KEY"}
print("Fetching system metrics...")
ErrorCounter = 0
response = httpx.get(URL, params=our_data, headers=headers)
code = response.status_code
if code == 200:
    server_data = response.json()
    # data = json.loads(server_data)
    user = server_data.get("user", {})
    name = server_data.get("name")
    email = server_data.get("email")
    address = server_data.get("address")
    city = address.get("city")
    street = address.get("street")
    print(name)
    print(email)
    print(f"{street}, {city}")
    sleep(10)
else:
    ErrorCounter+=1
    while (ErrorCounter < 3):
        if code == 200:
            server_data = response.json()
            # data = json.loads(server_data)
            user = server_data.get("user", {})
            name = server_data.get("name")
            email = server_data.get("email")
            address = server_data.get("address")
            city = address.get("city")
            street = address.get("street")
            print(name)
            print(email)
            print(f"{street}, {city}")
        response = httpx.get(URL, params=our_data, headers=headers)
        if code == 401:
            ErrorCounter += 1
        if ErrorCounter >= 3:
            print("Invalid API Key")
            print(f"Attempt {ErrorCounter} failed: Server is currently down.")

    if code == 500:
        print("Server is currently down.")
print("All retry attempts failed.")

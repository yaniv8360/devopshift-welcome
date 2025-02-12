import json
import httpx

URL = "https://jsonplaceholder.typicode.com/users/1"
headers = {"Authorization": "BEAFJDLGKJLKJ FDSGKJHFDSGKJH:LANF:LN"}
our_data = {"name": "ofer"}
response = httpx.get(URL)
# response = httpx.post(URL,"https://www.google.com", headers=headers, data={"name":"ofer"})
code = response.status_code
if code == 200:
    server_data = response.json()
    # data = json.loads(server_data)
    user = server_data.get("user", {})
    name = server_data.get("name")
    email = server_data.get("email")
    address = server_data.get("address")
    city=address.get("city")
    street=address.get("street")
    print(name)
    print(email)
    print(f"{street}, {city}")
if code == 400:
    server_data = response.json()
    print("User not found.")
if code == 500:
    server_data = response.json()
    print("Server error. Please try again later.")

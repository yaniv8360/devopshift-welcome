import httpx
from pprint import pprint

response = httpx.get("https://jsonplaceholder.typicode.com/users")
users = response.json()
for user in users:
    print(user["name"])
    
pprint(users[0])

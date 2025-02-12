# from log import setup_logging
from dataclasses import dataclass
from fastapi import FastAPI
# import httpx
from datetime import date, datetime

# logger = setup_logging()
app = FastAPI()
servers = ["nginx", "docker"]
servers_validity = {"nginx": True, "docker": False}


@dataclass
class User:
    name: str
    email: str
    d: datetime = datetime.now()


@app.get("/")
def hello_world(server_name :str):
    "This is our main function"
    # return {"result": ["hello world", 1, 2, 3, True, None], "error": False}
    return User("ofer", "ofer@ofer.com")

@app.get("/users")
def get_users() -> list[User]:
    response = httpx.get("https://jsonplaceholder.typicode.com/users")
    users = response.json()
    return users


@app.post("/servers")
def post_servers(server: str) -> bool:
    try:
        servers_validity[server]
    except KeyError:
        return False
    return servers_validity[server]


# @app.post("/users")
# def create_user(new_user:user) -> bool:
#     return True
# xfv
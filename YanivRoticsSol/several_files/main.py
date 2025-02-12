# # from log import setup_logging
# # from dataclasses import dataclass
# from fastapi import FastAPI
# # import httpx
# # from datetime import date, datetime
# from models import 

# # logger = setup_logging()
# app = FastAPI()
# servers = {"nginx": True, "docker": False}


# @dataclass
# class ServerStatusResponse:
#     server_name: str
#     server_status: str | bool


# @app.get("/server")
# def get_server(server_name: str) -> ServerStatusResponse:
#     server_status = servers.get(server_name, "Does not exist")
#     return ServerStatusResponse(server_name, server_status)


# @app.post("/server")
# def create_server(server_name: str)->ServerStatusResponse:
#     if server_name in servers:
#         return ServerStatusResponse(server_name, "name already exists")
#     else:
#         servers[server_name] = True
#         return ServerStatusResponse(server_name, "created")

# @app.get("/")
# def hello_world(server_name :str):
#     "This is our main function"
#     # return {"result": ["hello world", 1, 2, 3, True, None], "error": False}
#     return User("ofer", "ofer@ofer.com")

# @app.get("/users")
# def get_users() -> list[User]:
#     response = httpx.get("https://jsonplaceholder.typicode.com/users")
#     users = response.json()
#     return users


# @app.post("/servers")
# def post_servers(server: str) -> bool:
#     try:
#         Servers[server]
#     except KeyError:
#         return False
#     return Servers[server]


# @app.post("/users")
# def create_user(new_user:user) -> bool:
#     return True

from fastapi import FastAPI
from models import ServerStatusResponse, Server

app = FastAPI()


@app.get("/server")
def get_server(server_name: str) -> ServerStatusResponse:
    server_status = servers.get(server_name, "Does not exist")
    return ServerStatusResponse(server_name, server_status)


@app.post("/server")
def create_server(server_name: str) -> ServerStatusResponse:
    if server_name in servers:
        return ServerStatusResponse(server_name, "Name already exists")
    else:
        servers[server_name] = True
        return ServerStatusResponse(server_name, "Created")

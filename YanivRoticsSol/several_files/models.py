# # f = open("servers.txt", "r+")  # Changed from "rw" to "r+"
# # f.seek(6)
# # f.write("hello from python")
# # f.seek(6)          # Move the pointer back to read what was written, if needed.
# # data = f.read(30)
# # try:
# #     servers = [server.strip() for server in f.readlines()]
# #     print(servers)
# # finally:
# #     f.close()
# # from dataclasses import dataclass

# # class Server:
# #     name:str
# #     online:bool
# #     cpus:int
# #     ram:int

# from pydantic import BaseModel
# import json


# class Server(BaseModel):
#     name: str
#     online: bool
#     cpus: int
#     ram: int


# # s = Server("wow", True, 6, 10)

# with open("servers.txt", "r+") as f:
#     servers = []
#     for line in f.readline():
#         if line.strip():
#             json_object=json.loads(line)
#             new_server = Server(**json_object)
#             servers.append(new_server)
#     # print(type(servers[0]))
# # print(servers)
# # print(servers[0]["name"])

# with open("servers.txt", "a") as f:
#     new_server = Server(name="wow", online=True, cpus=6, ram=10)
#     # server_str= json.dumps(new_server)
#     f.write("\n")
#     f.write(new_server.model_dump_json())
#     # f.write("\n")

# # f.read() weill not worked
# # print("file already closed")

# from pydantic import BaseModel, ValidationError
# import json


# class Server(BaseModel):
#     name: str
#     online: bool
#     cpus: int
#     ram: int


# def read_server_list() -> list[Server]:
#     with open("servers.txt", "r+") as f:
#         servers = []
#         for line in f:
#             if line.strip():
#                 json_object = json.loads(line)
#                 try:
#                     new_server = Server(**json_object)
#                 except ValidationError:
#                     pass
#             else:
#                 servers.append(new_server)
#     # print(servers)
#     # print(servers[0].name)

#     for server in servers:
#         print(server)
# def add_new_server(server: Server):
#     with open("servers.txt", "a") as f:
#         new_server = Server(name="wow", online=True, cpus=6, ram=10)
#         f.write("\n")
#         f.write("\n")

from pydantic import BaseModel, ValidationError
import json


class ServerStatusResponse(BaseModel):
    server_name: str
    server_status: str | bool


class Server(BaseModel):
    name: str
    online: bool
    cpus: int
    ram: int


def read_server_list() -> list[Server]:
    with open("servers.txt", "r") as f:
        servers: list[Server] = []
        for line in f.readlines():
            if line.strip():
                json_object = json.loads(line)
                try:
                    new_server = Server(**json_object)
                except ValidationError:
                    pass
                else:
                    servers.append(new_server)
    return servers


def add_new_server(new_server: Server):
    with open("servers.txt", "a") as f:
        new_server = Server(name="wow", online=True, cpus=6, ram=10)
        f.write("\n")
        f.write(new_server.model_dump_json())

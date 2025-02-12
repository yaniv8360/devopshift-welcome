from distutils.core import setup
import logging

logger = setup_logging()
servers = {"nginX": True, "DoCkEr": False}

def get_server_status_2(server_name: str) -> bool:
    lowercase_servers = {key.strip().lower(): value for key,
                         value in servers.items()}
    if server_name in lowercase_servers:
        return lowercase_servers[server_name]
    else:
        logger.error(f"The server name {server_name} does not exist")


def get_server_status(server_name: str) -> bool:
    lowercase_servers = {key.strip().lower(): value for key,
                         value in servers.items()}
    try:
        return lowercase_servers[server_name]
    except KeyError:
        logger.error(f"The server name {server_name} does not exist")


def check_servers_from_terminal():
 
    while True:
        server_name = input("Enter server name: ").strip().lower()
        status = get_server_status(server_name)
        logger.info(f"Server {server_name} status is: {status}")

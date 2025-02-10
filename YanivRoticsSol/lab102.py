import os
import sys
import logging
import json

# Custom exception class for invalid server names
class InvalidServerNameError(Exception):
    pass

# Custom logging formatter to output logs as JSON
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {"time": record.created, "module": record.module, "message": record.msg}
        return json.dumps(log)

# Set up the logger
logger = logging.getLogger("myapp")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

log_level = os.environ.get("LOGLEVEL", "DEBUG").upper()
log_level = logging.getLevelName(log_level)  # Convert to logging level
log_format = "%(asctime)s:%(name)s: %(levelname)s: %(module)s:%(lineno)d:%(funcName)s: %(message)s"
logging.basicConfig(filename='myapp.log', format=log_format, level=log_level)

# Function to check the service status
def check_service_status(server_name):
    valid_servers = ["nginx", "docker"]
    if server_name in valid_servers:
        logger.info("The user has typed a valid server name.")
        return "Running"
    else:
        logger.error("Invalid server name entered.")
        raise ValueError("The user has typed an invalid server name.")

try:
    server_name = input("Enter server name: ").strip()
    if not server_name.isalnum():
        raise InvalidServerNameError("Server name must contain only alphanumeric characters.")
    status = check_service_status(server_name)
    print(f"Server status: {status}")

except InvalidServerNameError as e:
    logger.error(f"InvalidServerNameError: {e}")
    print(f"Error: {e}")

except ValueError as e:
    logger.error(f"ValueError: {e}")
    print(f"Error: {e}")

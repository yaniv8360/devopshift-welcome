valid_servers = ["nginx", "docker"]
try:
    server_name = input("Enter server name: ").strip()
    if not server_name.isalnum():
        raise ValueError("Invalid server name.")
    if server_name in valid_servers:
        print("Server is running.")
    else:
        print("Server not recognized.")
except ValueError as e:
    print(f"Error: {e}")
import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = "0.0.0.0"
    server_port = 9001

    print("Starting up on {} port {}".format(server_address, server_port))

    sock.bind((server_address, server_port))

    client_list = []

    while True:
        data, address = sock.recvfrom(4096)
        username_length = int.from_bytes(data[:1], "big")
        username = data[1:username_length + 1].decode("utf-8")
        message = data[username_length + 1:].decode("utf-8")

        print(f"{username}: {message}")

        if address in client_list:
            print(f"Already connected: {address}")
        else:
            client_list.append(address)
            print(f"New connection from {address}")

        for client in client_list:
            if client != address:
                sock.sendto(data, client)
                print(f"Sent message to {client}")


if __name__ == "__main__":
    main()
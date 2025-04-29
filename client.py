import socket
import sys
import threading

def protocol_header(username_length):
    return username_length.to_bytes(1, "big")

def send_message(sock, server_address, server_port, username):
    while True:
        input_message = input(f"{username}: ")
        if input_message.lower() == "exit":
            break
        message = protocol_header(len(username)) + (username + input_message).encode("utf-8")
        sock.sendto(message, (server_address, server_port))
        print(f"--- Sent: {input_message}")

    sock.close()
    sys.exit(0)

def receive_message(sock):
    while True:
        data, _ = sock.recvfrom(4096)
        username_length = int.from_bytes(data[:1], "big")
        username = data[1:username_length + 1].decode("utf-8")
        message = data[username_length + 1:].decode("utf-8")
        print(f"{username}: {message}")
        print(f"Received: {username}: {message}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = input("Type in the server's address to connect to: ")
    server_port = 9001
    
    address = ""
    port = 9050

    sock.bind((address, port))

    username = input("Type in your user name: ")
    message = protocol_header(len(username)) + username.encode("utf-8")
    sock.sendto(message, (server_address, server_port))
    print(f"{username} has connected to the server.")

    send_thread = threading.Thread(target=send_message, args=(sock, server_address, server_port, username))
    receive_thread = threading.Thread(target=receive_message, args=(sock,))
    send_thread.start()
    receive_thread.start()
    send_thread.join()
    receive_thread.join()


if __name__ == "__main__":
    main()
    
    



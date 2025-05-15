import socket
import sys
import threading

def protocol_header(username_length):
    return username_length.to_bytes(1, "big")

def send_message(sock, server_address, server_port, username):
    while True:
        input_message = input()
        
        message = protocol_header(len(username)) + (username + input_message).encode("utf-8")

        try:
            sock.sendto(message, (server_address, server_port))
            print(f"--- Sent: {input_message}")

        except Exception as e:
            print(f"Error sending message: {e}")
            sock.close()
            exit(1)
    
    sock.close()
    sys.exit(0)

def receive_message(sock):
    while True:
        try:
            data, _ = sock.recvfrom(4096)
            username_len = int.from_bytes(data[:1], "big")
            username = data[1:username_len + 1].decode("utf-8")
            message = data[username_len + 1:].decode("utf-8")
            print(f"[Received] {username}: {message}")

        except Exception as e:
            print(f"Error receiving message: {e}")
            sock.close()
            exit(1)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = input("Type in the server's address: ")
    server_port = 9001
    
    client_address = ""
    client_port = 0

    sock.bind((client_address, client_port))

    try:
        username = input("Type in your user name: ")
        message = protocol_header(len(username)) + username.encode("utf-8")
        sock.sendto(message, (server_address, server_port))
        print(f"{username} has connected to the server.")

        # thread を使用してメッセージの送受信を並列処理
        send_thread = threading.Thread(target=send_message, args=(sock, server_address, server_port, username))
        receive_thread = threading.Thread(target=receive_message, args=(sock,))
        send_thread.start()
        receive_thread.start()
        send_thread.join()
        receive_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nExiting...")
        sock.close()
        exit(1)

    finally:
        if sock:
            print("Closing client socket.")
            sock.close()

    sys.exit(0)


if __name__ == "__main__":
    main()
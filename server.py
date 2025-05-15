import socket
import sys
import threading
import datetime
import time

def remove_client(client_list):
    time.sleep(10) # サーバが起動してから10秒待機
    while True:
        addresses_to_remove = [] # 削除するクライアントのアドレスを格納するリスト
        current_time = datetime.datetime.now()

        for address in list(client_list.keys()):
            client_info = client_list.get(address)

            if client_info.get("last_send_time") is not None:
                # 経過時間を計算
                elapsed_seconds = (current_time - client_info["last_send_time"]).total_seconds()

                if (elapsed_seconds > 30):
                    print(f"Removing client {address} due to inactivity ({elapsed_seconds:.2f}s).")
                    addresses_to_remove.append(address)
        for address in addresses_to_remove:
            del client_list[address]
            # client_list.pop(address, None)
            
        time.sleep(5) # 5秒ごとにチェック

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = "0.0.0.0"
        server_port = 9001

        print("Starting up on {} port {}".format(server_address, server_port))

        sock.bind((server_address, server_port))

        # クライアントの情報を格納する辞書
        client_list = {}

        # thread を使用してクライアントの削除を並列処理
        removing_thread = threading.Thread(target=remove_client, args=(client_list,), daemon=True)
        removing_thread.start()

        while True:
            # クライアントからのメッセージを受信
            data, address = sock.recvfrom(4096)
            username_len = int.from_bytes(data[:1], "big")
            username = data[1:username_len + 1].decode("utf-8")
            message_content = data[username_len + 1:].decode("utf-8")

            print(f"Received from {address} (user: {username}): {message_content}")

            # クライアントの情報を更新または追加
            if address in client_list:
                client_list[address]["last_send_time"] = datetime.datetime.now()
                client_list[address]["username"] = username
            else:
                client_list[address] = {
                    "address": address,
                    "username": username,
                    "last_send_time": datetime.datetime.now()
                }
                print(f"New client connected from {address} (user: {username}). Total clients: {len(client_list)}")

            # メッセージを送った人を除く全クライアントに送信
            for client_address in client_list:
                if client_address != address and message_content:
                    try:
                        sock.sendto(data, client_address)
                    except Exception as e:
                        print(f"An error occurred sending to {client_address}: {e}")
    
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    
    except Exception as e:
        print(f"\nAn error occurred: {e}")

    finally:
        if sock:
            print("Closing server socket.")
            sock.close()

    print("Server shut down.")
    sys.exit(0)


if __name__ == "__main__":
    main()
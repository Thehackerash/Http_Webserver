import socket
from handler import handle_client 
from threading import Thread
import sys
import argparse
import gzip
import io

def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    print("Waiting for connection...")
    parser = argparse.ArgumentParser(description="A simple server script.")
    parser.add_argument('--directory', required=False, help="Directory to serve files from")
    args = parser.parse_args()
    directory = args.directory
    print(directory)
    thread = []
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")
        t = Thread(target=handle_client, args=[conn, directory])
        thread.append(t)
        t.run()

if __name__ == "__main__":
    main()

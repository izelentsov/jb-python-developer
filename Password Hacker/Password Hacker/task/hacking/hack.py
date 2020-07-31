# write your code here
import sys
import socket


def run(ip, port, msg):
    with socket.socket() as client:
        client.connect((ip, port))
        client.send(msg.encode())
        resp = client.recv(1024)
    print(resp.decode())


def main():
    args = sys.argv
    ip = args[1]
    port = int(args[2])
    msg = args[3]

    run(ip, port, msg)


main()

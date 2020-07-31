# write your code here
import sys
import socket
import string
from itertools import product, combinations

CHARS = string.digits + string.ascii_lowercase


def run(ip, port):
    p = brute(ip, port)
    if p is not None:
        print(p)


def brute(ip, port):
    with socket.socket() as client:
        client.connect((ip, port))

        pwds = generate_pwds()
        for p in pwds:
            client.send(p.encode())
            resp = client.recv(1024).decode()
            if resp == 'Connection success!':
                return p
            if resp == 'Too many attempts':
                return None


def generate_pwds():
    n = 1
    while True:
        pwds = gen_of_len(n)
        for p in pwds:
            yield ''.join(p)
        n += 1


def gen_of_len(n):
    return product(CHARS, repeat=n)


def main():
    args = sys.argv
    ip = args[1]
    port = int(args[2])

    run(ip, port)


main()

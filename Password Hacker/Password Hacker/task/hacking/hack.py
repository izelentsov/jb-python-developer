# write your code here
import sys
import socket
import string
from itertools import product, combinations

CHARS = string.digits + string.ascii_lowercase

NEXT_CONTINUE = 0
NEXT_STOP = 1


def run(ip, port):
    pwds = typical_pwds()
    p = check_pwds(pwds, ip, port)
    if p is not None:
        print(p)


def brute_pwds():
    n = 1
    while True:
        pwds = gen_of_len(n)
        for p in pwds:
            yield ''.join(p)
        n += 1


def gen_of_len(n):
    return product(CHARS, repeat=n)


def typical_pwds():
    typicals = read_typs()
    for t in typicals:
        yield from shuffle_cases(t)


def read_typs():
    with open("passwords.txt", "r") as f:
        for line in f:
            yield line.strip()


def shuffle_cases(w):
    cur = w.lower()
    while cur is not None:
        yield cur
        cur = next_case_shuffle(cur)


def next_case_shuffle(w):
    if len(w) == 0:
        return None
    prefix = w[:-1]
    last = w[-1]
    if last.isalpha():
        if last.islower():
            next_prefix = prefix
            next_last = last.upper()
        else:
            next_prefix = next_case_shuffle(prefix)
            next_last = last.lower()
    else:
        next_prefix = next_case_shuffle(prefix)
        next_last = last

    if next_prefix is None:
        return None
    return next_prefix + next_last



def check_pwds(pwds, ip, port):
    with socket.socket() as client:
        client.connect((ip, port))

        for p in pwds:
            client.send(p.encode())
            resp = client.recv(1024).decode()
            if resp == 'Connection success!':
                return p
            if resp == 'Too many attempts':
                return None


def main():
    args = sys.argv
    ip = args[1]
    port = int(args[2])

    run(ip, port)


main()

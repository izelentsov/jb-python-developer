import sys
import os
import collections
import requests


# write your code here


def run():

    store_dir = sys.argv[1]
    if not os.path.exists(store_dir):
        os.mkdir(store_dir)
    history = collections.deque()
    current = None

    while True:
        # print(f"State: {current}; {history}")
        cmd = input()
        if cmd == 'exit':
            break

        text, current = get_text(cmd, store_dir, history, current)

        if text:
            print(text)
        else:
            print("Error: Incorrect URL")


def get_text(cmd, store_dir, history, current):
    if cmd == 'back':
        cmd = go_back(history)
        if not cmd:
            return None, current
    elif current:
        history.append(current)

    text = get_stored(cmd, store_dir)
    if text:
        return text, cmd

    if is_url(cmd):
        text = get_url(cmd)
        if text:
            st_name = store(cmd, text, store_dir)
            return text, st_name

    return None, cmd


def go_back(history):
    if len(history) > 0:
        return history.pop()
    return None


def get_stored(cmd, store_dir):
    path = store_dir + '/' + cmd
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()
    return None


def is_url(cmd):
    return '.' in cmd


def get_url(url):
    url = clean_url(url)
    r = requests.get(url)
    return r.text


def clean_url(url):
    return url if url.startswith("https://") else "https://" + url


def store(url, text, store_dir):
    name = store_name(url)
    with open(store_dir + '/' + name, 'w') as f:
        f.write(text)
    return name


def store_name(url):
    s = url[8:] if url.startswith("https://") else url
    return s[:s.rindex('.')]


run()

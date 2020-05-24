import sys
import os
import collections
import requests
import bs4
import colorama
from colorama import Fore


colorama.init()


# write your code here
TAGS = {
    'p': {'block': True},
    'h1': {'block': True},
    'h2': {'block': True},
    'h3': {'block': True},
    'h4': {'block': True},
    'h5': {'block': True},
    'h6': {'block': True},
    'ul': {'block': True},
    'ol': {'block': True},
    'li': {'block': True},
    'a': {'block': False, 'fore': Fore.BLUE},
    'title': {'block': True}
}



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
            text = render(text)
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


def render(html):
    soup = bs4.BeautifulSoup(html, features="html.parser")
    return render_tag(soup.html)


def render_tag(tag):
    if tag.name in TAGS.keys():
        config = TAGS[tag.name]
        newline = config['block']
        color = config['fore'] if 'fore' in config else None
        return render_tag_text(tag, withtext=True, newline=newline, color=color)
    return render_tag_text(tag, withtext=False, newline=False)


def render_tag_text(p, withtext, newline, color=None):
    text = ''
    if color:
        text += color
    for part in p.contents:
        text += render_content(part, withtext=withtext)
    if color:
        text += Fore.RESET
    return text + ('\n' if newline else '')


def render_content(part, withtext):
    if isinstance(part, bs4.element.NavigableString):
        return str(part).strip() if withtext else ''
    return render_tag(part)


#print(render("<body><h1>h1</h1><p><a>1</a></p><p><a>2</a></p></body>"))
run()

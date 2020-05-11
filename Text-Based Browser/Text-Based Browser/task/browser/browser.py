import sys
import os

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

# write your code here

def run():

    store_dir = sys.argv[1]
    if not os.path.exists(store_dir):
        os.mkdir(store_dir)

    while True:
        cmd = input()
        if cmd == 'exit':
            break

        text = get_stored(cmd, store_dir)
        from_store = True
        if not text:
            from_store = False
            if is_url(cmd):
                text = get_url(cmd)
        if text:
            print(text)
            if not from_store:
                store(cmd, text, store_dir)
        else:
            print("Error: Incorrect URL")


def get_stored(cmd, store_dir):
    path = store_dir + '/' + cmd
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()
    return None


def is_url(cmd):
    return '.' in cmd


def get_url(url):
    text = None
    if url == 'nytimes.com':
        text = nytimes_com
    elif url == 'bloomberg.com':
        text = bloomberg_com
    return text


def store(url, text, store_dir):
    name = store_name(url)
    with open(store_dir + '/' + name, 'w') as f:
        f.write(text)


def store_name(url):
    return url[:url.rindex('.')]


run()

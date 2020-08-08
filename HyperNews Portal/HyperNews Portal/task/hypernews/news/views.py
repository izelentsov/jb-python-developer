from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
import json
import random


# Create your views here.
class NewsMainView(View):
    def get(self, request, *args, **kwargs):
        n = read_news_main(settings.NEWS_JSON_PATH)
        context = {
            'news': n
        }
        return render(request, 'news/main.html', context=context)


class NewsItemView(View):
    def get(self, request, news_link, *args, **kwargs):
        n = read_news(settings.NEWS_JSON_PATH, int(news_link))
        context = {
            "news": n
        }
        return render(request, 'news/item.html', context=context)


class NewsCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html', context={})

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        add_news(settings.NEWS_JSON_PATH, title, text)
        return redirect('/news/')


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<p>Coming soon</p>')


def read_all_news(path):
    with open(path, 'r') as f:
        return json.load(f)


def read_news_main(path):
    all_news = read_all_news(path)
    return group_by_date(all_news)


def read_news(path, link):
    all_news = read_all_news(path)
    for n in all_news:
        if n['link'] == link:
            return n
    return None


def add_news(path, title, text):
    all_news = read_all_news(path)
    links = to_links(all_news)
    n = create_news(title, text, links)
    all_news.append(n)
    write_news(path, all_news)


def create_news(title, text, links):
    link = gen_link(links)
    created = gen_created()
    return {
        'created': created,
        'link': link,
        'title': title,
        'text': text
    }


def gen_link(existing):
    link = random.randrange(1000000)
    while link in existing:
        link = random.randrange(1000000)
    return link


def gen_created():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def write_news(path, news):
    with open(path, "w") as f:
        json.dump(news, f)


def to_links(news):
    return {n['link'] for n in news}


def group_by_date(news):
    grouped = {}
    for n in news:
        d = n['created']
        day = d.split()[0]
        if day not in grouped:
            grouped[day] = []
        grouped[day].append(n)
    s = sorted(grouped.items(), key=lambda kv: kv[0], reverse=True)
    objs = [{'date': d, 'news': ns} for d, ns in s]
    return {'dates': objs}

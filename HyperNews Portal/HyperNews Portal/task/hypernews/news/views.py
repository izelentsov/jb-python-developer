from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.conf import settings
import json


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


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<p>Coming soon</p>')


def read_news_main(path):
    with open(path, 'r') as f:
        all_news = json.load(f)
        return group_by_date(all_news)


def read_news(path, link):
    with open(path, "r") as f:
        all_news = json.load(f)
        for n in all_news:
            if n['link'] == link:
                return n
    return None


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

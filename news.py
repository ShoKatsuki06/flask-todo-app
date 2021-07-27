import urllib.request
from bs4 import BeautifulSoup
from flask import Flask,render_template,request,redirect,url_for,session

def check():
    url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
    response = urllib.request.urlopen(url)

    html = BeautifulSoup(response, 'html.parser')
    topics = html.find_all("title")

    i = 0
    news=[]
    for item in topics:
        if i == 0:
            i+=1
        elif i<4:
            print(item.string)
            news.append(item.string)
            i+=1
        else:
            break
    return news

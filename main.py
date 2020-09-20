# coding: utf-8

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = "/usr/local/bin/chromedriver" # local
QIITA_BASE_URL = "https://qiita.com/"

SLACK_WEBHOOK_ENDPOINT = "https://hooks.slack.com/services/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"
SLACK_USER_NAME = "retro big bot"
SLACK_USER_ICON = ":robot_face:"

class QiitaArticle:
    def __init__(self, rank=None, url=None, title=None, like_count=None):
        self.rank = rank
        self.url = self.set_url(url)
        self.title = title
        self.like_count = like_count

    def set_url(self, path):
        return urljoin(QIITA_BASE_URL, path)

    def to_message(self):
        rank_message = "[ rank: {} ]".format(self.rank).ljust(12, " ")
        return rank_message + " <{}|{}> ( likes: {} )".format(self.url, self.title, self.like_count)

def create_driver(driver_path):
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    return webdriver.Chrome(executable_path=driver_path, chrome_options=options)

def get_html(endpoint):
    driver = create_driver(DRIVER_PATH)
    driver.get(endpoint)
    html = driver.page_source
    return html

def parse_qiita_daily(html):
    soup = BeautifulSoup(html, 'lxml')
    item_list = soup.find_all('div', {'class': 'tr-Item'})

    qiita_articles = []
    for i, item in enumerate(item_list):
        title_a = item.find('a', {'class': 'tr-Item_title'})
        likecount_div = item.find('div', {'class': 'tr-Item_likeCount'})

        url = title_a.get('href')
        title = title_a.get_text()
        likes = likecount_div.get_text()

        article = QiitaArticle(i+1, url, title, likes)
        qiita_articles.append(article)

    return qiita_articles

def post_to_slack(text):
    dict_json = {'username': SLACK_USER_NAME, 'icon_emoji': SLACK_USER_ICON, 'text': text}
    return requests.post(SLACK_WEBHOOK_ENDPOINT, headers={'Content-Type': 'application/json'}, json=dict_json)

endpoint = "https://qiita.com/"
html = get_html(endpoint)
articles = parse_qiita_daily(html)
full_message = "\n".join([art.to_message() for art in articles])

response = post_to_slack(full_message)


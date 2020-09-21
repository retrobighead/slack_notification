from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

QIITA_BASE_URL = "https://qiita.com/"

class WebDriver:
    def __init__(self, chrome_driver_url):
        self.chrome_driver_url = chrome_driver_url
        self.driver = self.get_driver()

    def get_driver(self):
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--proxy-server="direct://"')
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--start-maximized')
        options.add_argument('--headless')
        return webdriver.Chrome(executable_path=self.chrome_driver_url, chrome_options=options)

    def get_html(self, url):
        self.driver.get(url)
        html = self.driver.page_source
        return html

class QiitaParser:
    def __init__(self, chrome_driver_url):
        self.driver = WebDriver(chrome_driver_url)

    def get_qiita_daily(self):
        html = self.driver.get_html(QIITA_BASE_URL)

        soup = BeautifulSoup(html, 'lxml')
        item_list = soup.find_all('div', {'class': 'tr-Item'})

        qiita_articles = []
        for i, item in enumerate(item_list):
            title_a = item.find('a', {'class': 'tr-Item_title'})
            likecount_div = item.find('div', {'class': 'tr-Item_likeCount'})

            url = title_a.get('href')
            title = title_a.get_text()
            likes = likecount_div.get_text()

            article = QiitaArticle(i + 1, url, title, likes)
            qiita_articles.append(article)

        return qiita_articles

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
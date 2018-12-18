"""
    CommunistBadger v1.0.0
    This is the code for news collection from the online sources.
    We perform keyword search and fetch news from around the globe.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import validators
import time, requests
from collections import OrderedDict
import datetime

# Basic names and IO requirements.
cnbc_base_url = "https://www.cnbc.com/search/?query={}&qsearchterm={}"
file_csv = "articles/{}_{}_tweets_{}.csv"
yahoo_base_url = "https://finance.yahoo.com/quote/{}?p={}"

class NewsScrapper():
    def __init__(self, stockName, source):
        self.stockName = stockName
        self.source = source
        self.titles_lst = []
        self._current_stuff_ = datetime.datetime.now()
        self.time_date = self._current_stuff_.strftime("%Y-%m-%d-%H-%M")
        self.file_name_ = file_csv.format(self.time_date, self.stockName, self.source)
        self.file_name_ = open(self.file_name_, 'w')
        self.file_name_.write('Stock'+','+'Article'+'\n')

    def _get_cnbc_news(self):
        _scrap_url = cnbc_base_url.format(self.stockName,self.stockName)
        assert "query" in _scrap_url # asserting that it is a URL, else error.
        driver = webdriver.Chrome()
        driver.get(_scrap_url)
        for i in range(1, 10):  # scrolling for n times
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # infinite scrolling issue.
            time.sleep(4)
        page = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page, 'html.parser')
        titles = soup.find_all('span', attrs={'class': 'Card-title'})
        urls = soup.find_all('a', attrs={'class': 'resultlink'})
        for i in range(len(titles)):
            hrefs = str(urls[i]).split()[2]
            hrefs = hrefs.replace('href="', '').replace('"><div', '')
            if validators.url(hrefs.replace('"', '')):
                re = requests.get(hrefs.replace('"', ''))
                _local_soup = BeautifulSoup(re.content, 'html.parser')
                _local_titles = _local_soup.find('h1', attrs={'class': 'title'})
                if _local_titles is None:
                    _local_titles = titles[i].text
                    self.titles_lst.append(str(_local_titles))
                else:
                    self.titles_lst.append(str(_local_titles.text))
            else:
                self.titles_lst.append(str(titles[i].text))
        self.titles_lst = list(OrderedDict.fromkeys(self.titles_lst))  # remove duplicates
        for ix in self.titles_lst:
            ix = ix.replace('...', '')
            if ',' in ix:
                ix = ix.replace(',', '')
            self.file_name_.write(self.stockName+","+ix+"\n")
            print("Title: ", ix)
        self.file_name_.close()

    def get_yahoo_news(self):
        _scrap_url = yahoo_base_url.format(self.stockName, self.stockName)
        assert "q" in _scrap_url
        driver = webdriver.Chrome()
        driver.get(_scrap_url)
        for i in range(1, 10):  # scrolling for n times
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # infinite scrolling issue.
            time.sleep(4)
        page = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page, 'html.parser')
        titles = soup.find_all('h3', attrs={'class': 'Mb(5px)'})
        for title in titles:
            subUrl, title, _ = str(title).split('-->')
            title = title.replace('<!-- /react-text', '')
            self.titles_lst.append(title)
        for ix in self.titles_lst:
            ix = ix.replace('...', '')
            if ',' in ix:
                ix = ix.replace(',', '')
            self.file_name_.write(self.stockName + "," + ix + "\n")
            print("Title: ", ix)
        self.file_name_.close()

    def data_collector(self):
        if self.source == "cnbc":
            self._get_cnbc_news()
        else:
            self.get_yahoo_news()

if __name__ == '__main__':
    NS = NewsScrapper("AAPL", "yahoo")
    NS.data_collector()

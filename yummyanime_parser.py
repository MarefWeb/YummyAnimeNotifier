import requests
import os
from bs4 import BeautifulSoup as Bs


class YummyAnime:

    def __init__(self):
        self.url = 'https://yummyanime.club'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

    # Метод для получения списка из последних 9 новостей
    def get_news(self):
        r = requests.get(url=self.url, headers=self.headers)
        html = Bs(r.content, 'html.parser')

        news_title = [item.text for item in html.select('.update-title')]
        news_info = [item.text for item in html.select('.update-info')]
        news_link = [self.url + item['href'] for item in html.select('.update-list > li > a')]
        news_img_href = [item['src'] for item in html.select('.update-img')]
        news = []

        for i in range(10):
            news_img_link = self.url + news_img_href[i]
            news_img_name = os.path.basename(news_img_href[i])
            filename = 'img\\' + news_img_name

            news_item = {'title': news_title[i],
                         'info': news_info[i],
                         'link': news_link[i],
                         'img_name': news_img_name}

            response = requests.get(news_img_link, headers=self.headers)

            with open(filename, 'wb') as f:
                f.write(response.content)

            news.append(news_item)

        return news

    # Метод для проверки списка новостей, на новые новости, которые ранее не публиковались
    @staticmethod
    def check_news(news):
        with open('news.txt', 'r') as f:
            file_content = f.readline()

        if file_content != '':
            last_news = file_content.split('===')
            last_news = {'title': last_news[0],
                         'info': last_news[1],
                         'link': last_news[2],
                         'img_name': last_news[3]}

            if news[0] == last_news:
                return 'нету новостей'

            else:
                last_news_full_title = last_news['title'] + last_news['info']
                match_index = None

                for i, item in enumerate(news):
                    item_full_title = item['title'] + item['info']
                    if item_full_title == last_news_full_title:
                        match_index = i
                        break

                with open('news.txt', 'w') as f:
                    f.write(f"{news[0]['title']}==={news[0]['info']}==={news[0]['link']}==={news[0]['img_name']}")

                return reversed(news[:match_index])

        else:
            last_news = news[0]

            with open('news.txt', 'w') as f:
                f.write(f"{last_news['title']}==={last_news['info']}==={last_news['link']}==={last_news['img_name']}")

            return last_news

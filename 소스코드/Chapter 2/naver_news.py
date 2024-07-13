import requests
from bs4 import BeautifulSoup
import pandas as pd

def naver_news_crawler(keyword):
    base_url = "https://search.naver.com/search.naver"
    params = {
        'where': 'news',
        'query': keyword,
        'sm': 'tab_opt'
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.select('div.news_wrap.api_ani_send')
    news_data = []
    
    for article in articles[:5]:
        title_tag = article.select_one('a.news_tit')
        title = title_tag.get_text()
        press = article.select_one('a.info.press').get_text().strip()
        
        news_data.append({
            'title': title,
            'press': press,
        })
    
    return pd.DataFrame(news_data)

keyword = input("검색할 키워드를 입력하세요: ")
news_df = naver_news_crawler(keyword)

news_df.to_excel('naver_news.xlsx', index=False, engine='openpyxl')
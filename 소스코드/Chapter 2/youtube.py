from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

search_keyword = '파이썬'
youtube_search_url = f'https://www.youtube.com/results?search_query={search_keyword}'

driver = webdriver.Chrome()
driver.get(youtube_search_url)

time.sleep(2)

page_body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(3):
    page_body.send_keys(Keys.END)
    time.sleep(2)
    
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

titles = []
urls = []
views = []

for video in soup.select('a#video-title'):
    try:
        title = video.get('title')
        video_url = 'https://www.youtube.com' + video.get('href')
        
        aria_label = video.get('aria-label')
        view_start = aria_label.find('조회수') + 4
        view_end = aria_label.rfind('회')
        view_count = aria_label[view_start:view_end].strip().replace(',', '')
        
        if not view_count:
            continue
        
        titles.append(title)
        urls.append(video_url)
        views.append(int(view_count))
    except (AttributeError, ValueError, TypeError):
        continue
    
df = pd.DataFrame({'Title': titles, 'URL': urls, 'Views': views})

top_videos = df.sort_values(by='Views', ascending=False).head(5)

top_videos.to_excel('youtube.xlsx', index=False)

for index, row in top_videos.iterrows():
    print(f'제목: {row["Title"]}')
    print(f'URL: {row["URL"]}')
    print(f'조회수: {row["Views"]}')
    print('-' * 30)
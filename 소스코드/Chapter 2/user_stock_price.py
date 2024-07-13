import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# 1
def crawl_stock_data(stock_code, start_date):
   url = f'https://finance.naver.com/item/sise_day.naver?code={stock_code}'
 
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
   data = []
   today = datetime.datetime.now()
   start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

   page = 1
   while True:
       response = requests.get(f'{url}&page={page}', headers=headers)
       html = response.text
       soup = BeautifulSoup(html, 'html.parser')
       table = soup.find('table', class_='type2')

       rows = table.find_all('tr')
       for row in rows:
           cols = row.find_all('td')
           if len(cols) < 7:
               continue

           date = cols[0].text.strip()
           if date == '':
               continue

           date_dt = datetime.datetime.strptime(date, '%Y.%m.%d')
           if date_dt < start_date:
               break

           if date_dt <= today:
               data.append({
                   'date': date,
                   'close': cols[1].text.strip().replace(',', ''),
                   'open': cols[3].text.strip().replace(',', ''),
                   'high': cols[4].text.strip().replace(',', ''),
                   'low': cols[5].text.strip().replace(',', ''),
                   'volume': cols[6].text.strip().replace(',', '')
               })

       if date_dt < start_date:
           break
       page += 1

   df = pd.DataFrame(data)
   df['date'] = pd.to_datetime(df['date'])
   return df

stock_code = input("종목 코드를 입력하세요 (예: 005930): ")
start_date = input("시작 날짜를 입력하세요 (YYYY-MM-DD 형식): ")

stock_data = crawl_stock_data(stock_code, start_date)

stock_data.to_csv('user_stock_price.csv', index=False)
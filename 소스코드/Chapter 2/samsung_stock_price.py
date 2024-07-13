import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

url = 'https://finance.naver.com/item/sise_day.naver?code=005930'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

data = []

today = datetime.now()
one_month_ago = today - timedelta(days=30)

for page in range(1, 5):
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
        try:
            date_parsed = datetime.strptime(date, '%Y.%m.%d')
        except ValueError:
            continue
        
        if one_month_ago <= date_parsed <= today:
            data.append({
                'date': date,
                'close': cols[1].text.strip().replace(',', ''),
                'open': cols[3].text.strip().replace(',', ''),
                'high': cols[4].text.strip().replace(',', ''),
                'low': cols[5].text.strip().replace(',', ''),
                'volume': cols[6].text.strip().replace(',', '')
            })

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

print(df)
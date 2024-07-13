import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://finance.naver.com/item/sise_day.naver?code=005930'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
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
        if one_month_ago <= date_parsed <= today: # 1
            data.append({
                'date': date,
                'close': float(cols[1].text.strip().replace(',', '')),
                'open': float(cols[3].text.strip().replace(',', '')),
                'high': float(cols[4].text.strip().replace(',', '')),
                'low': float(cols[5].text.strip().replace(',', '')),
                'volume': int(cols[6].text.strip().replace(',', ''))
            })

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

def get_color(value, min_val, max_val):
    normalized = (value - min_val) / (max_val - min_val)
    red = int(normalized * 255)
    blue = int((1 - normalized) * 255)
    return f'background-color: rgb({red}, 0, {blue});'

min_close, max_close = df['close'].min(), df['close'].max()
min_open, max_open = df['open'].min(), df['open'].max()
min_high, max_high = df['high'].min(), df['high'].max()
min_low, max_low = df['low'].min(), df['low'].max()
min_volume, max_volume = df['volume'].min(), df['volume'].max()

html_table = '<table border="1" style="border-collapse:collapse;">'
html_table += '<tr><th>Date</th><th>Close</th><th>Open</th><th>High</th><th>Low</th><th>Volume</th></tr>'
for index, row in df.iterrows():
    html_table += '<tr>'
    html_table += f'<td>{row["date"].strftime("%Y-%m-%d")}</td>'
    html_table += f'<td style="{get_color(row["close"], min_close, max_close)}">{row["close"]}</td>'
    html_table += f'<td style="{get_color(row["open"], min_open, max_open)}">{row["open"]}</td>'
    html_table += f'<td style="{get_color(row["high"], min_high, max_high)}">{row["high"]}</td>'
    html_table += f'<td style="{get_color(row["low"], min_low, max_low)}">{row["low"]}</td>'
    html_table += f'<td style="{get_color(row["volume"], min_volume, max_volume)}">{row["volume"]}</td>'
    html_table += '</tr>'
html_table += '</table>'

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = '여기에 본인의 gmail 주소를 입력합니다.'
smtp_password = '여기에 본인의 앱 비밀번호를 입력합니다.'
recipient_email = '여기에 수신 메일 주소를 입력합니다.'
subject = f'{today.strftime("%Y-%m-%d")} 삼성전자 주식 데이터'
body = f'''
<html>
  <body>
    <p>아래 표는 지난 한 달 동안의 삼성전자 주식 데이터를 보여줍니다.</p>
    {html_table}
  </body>
</html>
'''

msg = MIMEMultipart('alternative')
msg['From'] = smtp_username
msg['To'] = recipient_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'html'))

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)
server.sendmail(smtp_username, recipient_email, msg.as_string())
server.quit()

print('이메일 발송 완료!')
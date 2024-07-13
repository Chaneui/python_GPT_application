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
df['close'] = df['close'].astype(float)

html_table = df.to_html(index=False)

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
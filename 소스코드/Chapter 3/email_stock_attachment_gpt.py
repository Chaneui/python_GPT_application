import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

folder_path = r'여기에 ABNB_stock_by_date 폴더의 경로를 입력합니다.'
zip_file_path = 'ABNB_stock_by_date.zip'

with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, folder_path))

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = '여기에 본인의 gmail 주소를 입력합니다.'
smtp_password = '여기에 본인의 앱 비밀번호를 입력합니다.'
recipient_emails = ['AAAAA@naver.com', 'BBBBB@naver.com']
cc_emails = ['CCCCC@naver.com']
subject = 'ABNB Stock Data'
body = '''
<html>
  <body>
    <p>ABNB 주식 데이터가 첨부 파일로 포함되어 있습니다.</p>
  </body>
</html>
'''

msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = ', '.join(recipient_emails)
msg['Cc'] = ', '.join(cc_emails)
msg['Subject'] = subject

msg.attach(MIMEText(body, 'html'))

with open(zip_file_path, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file_path)}')
    msg.attach(part)

all_recipients = recipient_emails + cc_emails

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, all_recipients, msg.as_string())

print('이메일 발송 완료!')
import pytesseract
from PIL import Image
import requests


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = r'여기에 텍스트를 추출할 이미지의 경로를 입력합니다'

image = Image.open(image_path)

custom_config = r'--psm 6'
text = pytesseract.image_to_string(image, config=custom_config, lang='kor')

print("Extracted Text:\n", text)

# 1
KAKAO_API_KEY = '여기에 KoGPT 앱 키를 입력합니다'
KAKAO_API_URL = 'https://api.kakaobrain.com/v1/inference/kogpt/generation'

# 2
headers = {
    "Content-Type": "application/json",
    "Authorization": f"KakaoAK {KAKAO_API_KEY}"
}

# 3
data = {
    "prompt": text,
    "max_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.9,
    "n": 1,
    # "stop": ["\n"]
}

# 4
response = requests.post(KAKAO_API_URL, headers=headers, json=data)

# 5
if response.status_code == 200:
    summary = response.json().get('generations')[0].get('text')
    print("KoGPT:\n", summary)
else:
    print("Error:", response.status_code, response.text)

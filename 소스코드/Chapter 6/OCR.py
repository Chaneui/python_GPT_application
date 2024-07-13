import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = r'이 곳에 텍스트를 추출할 이미지 파일의 경로를 입력합니다'

image = Image.open(image_path)

custom_config = r'--psm 6'
text = pytesseract.image_to_string(image, config=custom_config, lang='eng')

print(text)
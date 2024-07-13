import os
from PIL import Image
import pillow_heif

folder_path = r'이 곳에 포맷을 변환할 파일의 경로를 지정합니다'
convert_path = r'이 곳에 포맷을 변환한 파일을 저장할 경로를 지정합니다'

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".heic"):
        heic_file_path = os.path.join(folder_path, filename)
        jpg_file_path = convert_path + '\\'+ filename.split('.')[0] + ".jpg"

        heif_file = pillow_heif.open_heif(heic_file_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(jpg_file_path, "JPEG")
        print(f"Converted {heic_file_path} to {jpg_file_path}")
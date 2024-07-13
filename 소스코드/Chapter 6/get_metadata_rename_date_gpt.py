import os
import shutil
from pillow_heif import register_heif_opener, open_heif
import piexif

register_heif_opener()

# 원본 폴더와 대상 폴더 경로 설정
source_folder = r'이 곳에 원본 이미지 파일이 위치한 폴더의 경로를 입력합니다'
target_folder = r'이 곳에 파일명을 변환 후 저장할 폴더의 경로를 입력합니다'

os.makedirs(target_folder, exist_ok=True)

for filename in os.listdir(source_folder):
    if filename.lower().endswith('.heic'):
        source_path = os.path.join(source_folder, filename)

        try:
            heif_file = open_heif(source_path)
        except Exception as e:
            print(f"Error opening {filename}: {e}")
            continue

        metadata = heif_file.info.get('exif')
        
        if metadata:
            exif_dict = piexif.load(metadata)
            date_time_original = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal)
            if date_time_original:
                date_str = date_time_original.decode("utf-8").split(" ")[0].replace(":", "")
                year = date_str[:4]
                year_folder = os.path.join(target_folder, year)
                os.makedirs(year_folder, exist_ok=True)
                
                new_filename = f"{date_str}_{filename}"
                target_path = os.path.join(year_folder, new_filename)

                try:
                    shutil.copy2(source_path, target_path)
                    print(f"Renamed and copied {filename} to {new_filename}")
                except Exception as e:
                    print(f"Error copying {filename} to {new_filename}: {e}")
            else:
                print(f"No DateTimeOriginal found in {filename}")
        else:
            print(f"No EXIF metadata found in {filename}")
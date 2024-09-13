import os
import shutil
import re

# 1
input_folder = r'이 곳에 폴더 경로를 입력합니다'

file_pattern = re.compile(r"^\d{4}-\d{2}\.csv$")

files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# 2
even_year_folder = os.path.join(input_folder, "짝수 연도")
odd_year_folder = os.path.join(input_folder, "홀수 년도")

# 3
if not os.path.exists(even_year_folder):
    os.makedirs(even_year_folder)
if not os.path.exists(odd_year_folder):
    os.makedirs(odd_year_folder)

for file in files:
    if file_pattern.match(file):
        
        # 4
        year = int(file[:4])
        if year % 2 == 0:
            dest_folder = even_year_folder
        else:
            dest_folder = odd_year_folder
        
        # 5
        src_file_path = os.path.join(input_folder, file)
        dest_file_path = os.path.join(dest_folder, file)
        shutil.copy2(src_file_path, dest_file_path)

import os
import shutil
import re

# 1
input_folder = '이 곳에 csv 파일이 위치한 폴더의 경로를 입력합니다'
output_folder = os.path.join(input_folder, '수정')

file_pattern = re.compile(r"^\d{4}-\d{2}\.csv$")

# 2
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

# 3
month_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# 4
for file in files:
    src_file_path = os.path.join(input_folder, file)
    dest_file_path = os.path.join(output_folder, file)
    shutil.copy2(src_file_path, dest_file_path)

    # 5
    if file_pattern.match(file):
        year = file[:4]
        month = int(file[5:7])
        month_name = month_abbr[month - 1]
        new_file_name = f"{month_name}-{year}.csv"
        new_file_path = os.path.join(output_folder, new_file_name)

        # 6
        os.rename(dest_file_path, new_file_path)
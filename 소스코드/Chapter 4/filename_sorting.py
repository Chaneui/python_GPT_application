import os
import shutil
import re

input_folder = r'이 곳에 폴더 경로를 입력합니다'

file_pattern = re.compile(r"^\d{4}-\d{2}\.csv$")

files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

for file in files:
    if file_pattern.match(file):
        year = file[:4]
        year_directory = os.path.join(input_folder, year)

        if not os.path.exists(year_directory):
            os.makedirs(year_directory)

        src_file_path = os.path.join(input_folder, file)
        dest_file_path = os.path.join(year_directory, file)
        shutil.copy2(src_file_path, dest_file_path)
import os
import openpyxl

def process_excel_files(folder_path):
    summary = {} 

    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.worksheets[0]
            modifications = 0

            for row in sheet.iter_rows(min_col=2, max_col=3, min_row=1):
                if row[0].value == "박승의":
                    row[1].value = 25
                    modifications += 1

            new_filename = f"{filename.rsplit('.', 1)[0]}_new.xlsx"
            new_file_path = os.path.join(folder_path, new_filename)
            workbook.save(new_file_path)

            summary[filename] = modifications

    return summary

def print_summary(summary):
    for filename, modifications in summary.items():
        print(f"{filename}: {modifications} modifications")

folder_path = r"이 곳에 엑셀 파일의 경로를 입력합니다"

summary = process_excel_files(folder_path)
print_summary(summary)
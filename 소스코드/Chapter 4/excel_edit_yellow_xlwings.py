import os
import xlwings as xw

def process_excel_files(folder_path):
    summary = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            workbook = xw.Book(file_path)
            sheet = workbook.sheets[0]

            # 3
            new_workbook = xw.Book()
            new_sheet = new_workbook.sheets[0]
            new_sheet.range('A1').value = sheet.range('A1').expand().value 

            modifications = 0

            for cell in new_sheet.range('B1').expand('down'):
                if cell.value == "박승의":
                    cell.offset(0, 1).value = 25
                    cell.offset(0, 1).color = (255, 255, 0)
                    modifications += 1

            new_filename = f"{filename.rsplit('.', 1)[0]}_new.xlsx"
            new_file_path = os.path.join(folder_path, new_filename)
            new_workbook.save(new_file_path)
            new_workbook.close()
            workbook.close()

            summary[filename] = modifications

    return summary

def print_summary(summary):
    for filename, modifications in summary.items():
        print(f"{filename}: {modifications} modifications")

folder_path = r"여기에 엑셀 파일이 있는 폴더의 경로를 입력합니다"

summary = process_excel_files(folder_path)
print_summary(summary)
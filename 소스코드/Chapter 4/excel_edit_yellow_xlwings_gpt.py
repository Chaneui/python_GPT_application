import os
import xlwings as xw

def process_excel_files(folder_path):
    summary = {}

    new_workbook = xw.Book()
    new_workbook.save(os.path.join(folder_path, "xlwings_수정.xlsx"))

    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx") and filename != "xlwings_수정.xlsx":
            file_path = os.path.join(folder_path, filename)
            workbook = xw.Book(file_path)
            sheet = workbook.sheets[0]

            new_sheet = new_workbook.sheets.add(name=filename.rsplit('.', 1)[0])
            new_sheet.range('A1').value = sheet.range('A1').expand().value

            modifications = 0

            for cell in new_sheet.range('B1').expand('down'):
                if cell.value == "박승의":
                    cell.offset(0, 1).value = 25
                    cell.offset(0, 1).color = (255, 255, 0)
                    modifications += 1

            workbook.close()

            summary[filename] = modifications

    new_workbook.save()
    new_workbook.close()

    return summary

def print_summary(summary):
    for filename, modifications in summary.items():
        print(f"{filename}: {modifications} modifications")

folder_path = r"이 곳에 엑셀 파일의 경로를 입력합니다"

summary = process_excel_files(folder_path)
print_summary(summary)

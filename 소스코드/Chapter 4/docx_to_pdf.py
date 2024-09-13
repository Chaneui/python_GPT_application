import os
import win32com.client

def convert_docx_to_pdf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    word = win32com.client.Dispatch("Word.Application")
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".docx"):
            full_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".pdf")
            
            doc = word.Documents.Open(full_file_path)
            
            doc.SaveAs(output_file_path, FileFormat=17)
            
            doc.Close()
    
    word.Quit()

input_folder = r"여기에 변환할 ppt 파일이 존재하는 경로를 입력합니다"
output_folder = r"여기에 변환한 PDF 파일을 저장할 경로를 입력합니다"
convert_docx_to_pdf(input_folder, output_folder)
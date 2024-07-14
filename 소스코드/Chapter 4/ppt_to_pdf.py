import os
import win32com.client

def convert_pptx_to_pdf(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".pptx"):
            full_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".pdf")
            
            presentation = powerpoint.Presentations.Open(full_file_path)
            
            presentation.SaveAs(output_file_path, 32)
            
            presentation.Close()
    
    powerpoint.Quit()

input_folder = r"여기에 변환할 ppt 파일이 존재하는 경로를 입력합니다"
output_folder = r"여기에 변환한 PDF 파일을 저장할 경로를 입력합니다"
convert_pptx_to_pdf(input_folder, output_folder)
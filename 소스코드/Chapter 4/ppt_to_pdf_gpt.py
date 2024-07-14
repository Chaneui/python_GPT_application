import os
import win32com.client

def merge_pptx_files(input_folder, output_pptx_path, output_pdf_path):
    if not os.path.exists(input_folder):
        print(f"The folder {input_folder} does not exist.")
        return
    
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1

    ppt_files = [f for f in os.listdir(input_folder) if f.endswith(".pptx")]
    ppt_files.sort()
    
    if not ppt_files:
        print("No PPTX files found in the folder.")
        return
    
    merged_presentation_path = os.path.join(input_folder, ppt_files[0])
    merged_presentation = powerpoint.Presentations.Open(merged_presentation_path)
    
    for filename in ppt_files[1:]:
        full_file_path = os.path.join(input_folder, filename)
        new_presentation = powerpoint.Presentations.Open(full_file_path)
        
        for slide in new_presentation.Slides:
            slide.Copy()
            merged_presentation.Slides.Paste(Index=len(merged_presentation.Slides) + 1)
        
        new_presentation.Close()
    
    merged_presentation.SaveAs(output_pptx_path)
    
    merged_presentation.SaveAs(output_pdf_path, 32)
    
    merged_presentation.Close()
    powerpoint.Quit()
    print('Merged files created.')

input_folder = r"여기에 변환할 ppt 파일이 존재하는 경로를 입력합니다"
output_pptx_path = os.path.join(input_folder, "mergedppt.pptx")
output_pdf_path = os.path.join(input_folder, "mergedpdf.pdf")

merge_pptx_files(input_folder, output_pptx_path, output_pdf_path)
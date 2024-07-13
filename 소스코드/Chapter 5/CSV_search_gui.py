import sys
import os
import pandas as pd
from PyQt5 import QtWidgets, uic

# 1
class CSVKeywordSearchApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(CSVKeywordSearchApp, self).__init__()
        # 2
        uic.loadUi(r'이 곳에 ui 파일 경로를 입력해야 합니다', self)

        # 3
        self.input_folder = self.findChild(QtWidgets.QLineEdit, 'input_folder')
        self.keyword = self.findChild(QtWidgets.QLineEdit, 'keyword')
        self.search_button = self.findChild(QtWidgets.QPushButton, 'search_button')
        self.result_display = self.findChild(QtWidgets.QTextBrowser, 'result_display')

        # 4
        self.search_button.clicked.connect(self.search_keyword_in_csv)

    # 5
    def search_keyword_in_csv(self):
        folder_path = self.input_folder.text()
        search_keyword = self.keyword.text()
        self.result_display.clear()

        # 6
        if not os.path.isdir(folder_path):
            self.result_display.append("유효한 폴더 경로를 입력하세요.")
            return

        # 7
        if not search_keyword:
            self.result_display.append("검색 키워드를 입력하세요.")
            return

        # 8
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        if not csv_files:
            self.result_display.append("해당 폴더에 CSV 파일이 없습니다.")
            return

        # 9
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            try:
                df = pd.read_csv(file_path)
                keyword_count = df.apply(lambda row: row.astype(str).str.contains(search_keyword).sum(), axis=1).sum()
                self.result_display.append(f"{csv_file}에 '{search_keyword}' 데이터가 {keyword_count}개 존재합니다.")
            except Exception as e:
                self.result_display.append(f"{csv_file}를 처리하는 중 오류 발생: {e}")

# 10
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CSVKeywordSearchApp()
    window.show()
    sys.exit(app.exec_())
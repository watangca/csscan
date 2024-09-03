import os
import json
from qt_core import *
from gui.widgets import *
from gui.database.DatabaseManager import DatabaseManager
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from datetime import datetime

class Page4WordWidget(QWidget):
    def __init__(self):
        super().__init__()

        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

        # DATABASE MANAGER INSTANCE
        self.db_manager = DatabaseManager()

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)

        # New Report Button with Spacer to push it to the right
        self.btn_new_report = PyPushButton("New Report")
        self.btn_new_report.clicked.connect(self.open_report_dialog)

        # Delete Report History 버튼 추가
        self.btn_delete_history = PyPushButton("Delete Report")
        self.btn_delete_history.clicked.connect(self.delete_report)

        # 버튼 레이아웃 구성
        button_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)
        button_layout.addWidget(self.btn_new_report)
        button_layout.addWidget(self.btn_delete_history) 
        
        # Report Table Widget
        self.report_table = PyTableWidget()
        self.report_table.setColumnCount(5)
        self.report_table.setHorizontalHeaderLabels(['리포트 템플릿', '리포팅 대상', '생성일시', 'STATUS', 'DOWNLOAD'])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add widgets to layout
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.report_table)

    def open_report_dialog(self):
        # 리포트 생성 다이얼로그를 여는 메소드
        dialog = PyReportDialog()
        dialog.exec()

        # 다이얼로그에서 데이터 가져오기
        if dialog.result() == QDialog.Accepted:
            template, target = dialog.get_report_info()
            self.add_report_to_table(template, target)

    def add_report_to_table(self, template, target):
        # 테이블에 리포트 정보를 추가하는 메소드
        row_position = self.report_table.rowCount()
        self.report_table.insertRow(row_position)

        # Add report details to the table
        self.report_table.setItem(row_position, 0, QTableWidgetItem(template))
        self.report_table.setItem(row_position, 1, QTableWidgetItem(target))
        self.report_table.setItem(row_position, 2, QTableWidgetItem(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.report_table.setItem(row_position, 3, QTableWidgetItem("Pending"))

        # Add export button to the table
        btn_export = PyPushButton(text="Export", radius=8, color=self.themes['app_color']['icon_color'])
        btn_export.clicked.connect(lambda *_: self.export_report(row_position))
        self.report_table.setCellWidget(row_position, 4, btn_export)

    def create_center_aligned_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def get_report_history_file_path(self):
        # 스크립트 파일이 위치한 디렉토리를 기준으로 상대 경로를 설정
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "report_history.json")
        return file_path

    def save_report_history(self):
        # 현재 테이블의 데이터를 파일에 저장
        report_history = []
        for row in range(self.report_table.rowCount()):
            report = {
                "template": self.report_table.item(row, 0).text(),
                "target": self.report_table.item(row, 1).text(),
                "date": self.report_table.item(row, 2).text(),
                "status": self.report_table.item(row, 3).text()
            }
            report_history.append(report)

        file_path = self.get_report_history_file_path()
        
        with open(file_path, "w") as file:
            json.dump(report_history, file)

    def delete_report(self):
        selected_items = self.report_table.selectedItems()
        if not selected_items:
            print("선택된 리포트가 없습니다.")
            return

        # 선택된 행의 인덱스를 얻기
        row = selected_items[0].row()

        # 테이블에서 해당 행 삭제
        self.report_table.removeRow(row)

        # report_history.json에서 해당 리포트 삭제
        self.update_report_history()

    def update_report_history(self):
        # 현재 테이블의 데이터를 다시 파일에 저장
        report_history = []
        for row in range(self.report_table.rowCount()):
            report = {
                "template": self.report_table.item(row, 0).text(),
                "target": self.report_table.item(row, 1).text(),
                "date": self.report_table.item(row, 2).text(),
                "status": self.report_table.item(row, 3).text()
            }
            report_history.append(report)

        with open("report_history.json", "w") as file:
            json.dump(report_history, file)

    def load_report_history(self):
        file_path = self.get_report_history_file_path()

        # 기존에 테이블에 있는 항목들을 모두 제거
        self.report_table.setRowCount(0)

        try:
            with open(file_path, "r") as file:
                report_history = json.load(file)
                for report in report_history:
                    self.add_report_to_table(report["template"], report["target"], report["date"], report["status"])
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
            pass  # 파일이 없으면 아무것도 하지 않음


    def export_report(self, row):
        # 리포트를 내보내는 메소드
        # 이 메소드는 실제 리포트 파일을 생성하고 사용자가 다운로드할 수 있도록 처리해야 함
        pass


import os
import openpyxl  
from qt_core import *
from gui.database.DatabaseManager import DatabaseManager
from gui.widgets import *
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes


class Page5WindowsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

        main_layout = QVBoxLayout(self)

        # Export 버튼과 PyTableWidget 생성 및 레이아웃 설정
        button_layout = QHBoxLayout()
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)

        self.export_button = PyPushButton("Export")
        self.export_button.clicked.connect(self.export_data_to_excel)
        button_layout.addWidget(self.export_button)

        main_layout.addLayout(button_layout)

        self.table_widget = PyTableWidget()
        main_layout.addWidget(self.table_widget)

        # 데이터 로드 및 테이블 구성
        self.load_data_into_table()

    def load_data_into_table(self):
        # 데이터베이스에서 데이터 가져오기
        windows_checklist_data = self.db_manager.fetch_all_data('windows_checklist')

        # 열의 수 설정 (5개)
        column_count = 5

        # 테이블의 행과 열 설정
        self.table_widget.setRowCount(len(windows_checklist_data))
        self.table_widget.setColumnCount(column_count)

        # 열 제목 설정
        self.table_widget.setHorizontalHeaderLabels(['NO', '카테고리', '점검항목', '심각도', '가이드'])

        # 테이블에 데이터 채우기
        for row_number, row_data in enumerate(windows_checklist_data):
            for column_number in range(column_count):
                item = QTableWidgetItem(str(row_data[column_number]))
                if column_number in [0, 1, 3]:  # 'NO', '카테고리', '심각도' 중앙 정렬
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table_widget.setItem(row_number, column_number, item)

        # 모든 열을 테이블 너비에 맞게 조정
        header = self.table_widget.horizontalHeader()
        for column in range(column_count):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    def export_data_to_excel(self):
        # 템플릿 파일 경로 설정
        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(current_dir, "windowsguide.xlsx")
        if not os.path.exists(template_path):
            PyDialog.warning(self, '경고', '템플릿 파일이 존재하지 않습니다.')
            return

        # Excel 파일 로드 및 데이터 작성
        workbook = openpyxl.load_workbook(template_path)
        sheet = workbook.active

        windows_checklist_data = self.db_manager.fetch_all_data('windows_checklist')
        for idx, row_data in enumerate(windows_checklist_data, start=2):
            for col_idx, value in enumerate(row_data[:5], start=1):
                sheet.cell(row=idx, column=col_idx, value=value)

        # 사용자에게 파일 저장 위치 선택 요청
        filename = os.path.join(os.path.expanduser('~'), 'Documents', 'windows_guideline.xlsx')
        filepath, _ = QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")

        if filepath:
            workbook.save(filepath)
            PyDialog.information(self, '알림', '파일이 저장되었습니다.')
        else:
            PyDialog.warning(self, '경고', '파일 저장이 취소되었습니다.')
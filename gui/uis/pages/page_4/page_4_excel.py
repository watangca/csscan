import os
import openpyxl
from qt_core import *
from gui.widgets import *
from datetime import datetime
from openpyxl.styles import Font
from gui.core.json_themes import Themes
from gui.core.json_settings import Settings
from gui.database.DatabaseManager import DatabaseManager



class Page4ExcelWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.db_manager = DatabaseManager()

        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

        # Setup UI
        self.setup_ui()
        self.load_report_history() 

    def setup_ui(self):
        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)

        self.btn_new_report = PyPushButton("New Report")
        self.btn_new_report.clicked.connect(self.open_report_dialog)

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
            report_info = dialog.get_report_info()
            template, target = report_info["template"], report_info["target"]
            self.add_report_to_table(template, target)

    def add_report_to_table(self, template, target, date=None, status="Pending"):

        row_position = self.report_table.rowCount()
        self.report_table.insertRow(row_position)

        # Add report details to the table with center alignment
        self.report_table.setItem(row_position, 0, self.create_center_aligned_item(template))
        self.report_table.setItem(row_position, 1, self.create_center_aligned_item(target))
        
        # 현재 날짜와 시간을 기본값으로 설정, 주어진 date가 없는 경우
        date = date if date else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.report_table.setItem(row_position, 2, self.create_center_aligned_item(date))
        self.report_table.setItem(row_position, 3, self.create_center_aligned_item(status))
        
        # Add export button to the table
        btn_export = PyTableButton("Export")
        btn_export.setFixedSize(75, 20)
        btn_export.clicked.connect(lambda *_: self.export_report(row_position))

        # 버튼을 테이블 셀 내 중앙에 배치하기 위한 위젯 및 레이아웃 설정
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(btn_export)
        layout.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        layout.setContentsMargins(0, 0, 0, 0)  # 마진 제거

        self.report_table.setCellWidget(row_position, 4, widget)

        # 새로운 리포트 정보를 데이터베이스에 저장
        self.db_manager.add_report_history(template, target, date, status)

    def create_center_aligned_item(self, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def save_report_history(self):
        for row in range(self.report_table.rowCount()):
            template = self.report_table.item(row, 0).text()
            target = self.report_table.item(row, 1).text()
            date = self.report_table.item(row, 2).text()
            status = self.report_table.item(row, 3).text()
            self.db_manager.add_report_history(template, target, date, status)

    def load_report_history(self):
        self.report_table.setRowCount(0)
        report_history = self.db_manager.get_all_report_history()
        for id, template, target, date, status in report_history:
            row_position = self.report_table.rowCount()
            self.report_table.insertRow(row_position)
            self.report_table.setItem(row_position, 0, self.create_center_aligned_item(template))
            self.report_table.setItem(row_position, 1, self.create_center_aligned_item(target))
            self.report_table.setItem(row_position, 2, self.create_center_aligned_item(date))
            self.report_table.setItem(row_position, 3, self.create_center_aligned_item(status))
            # Assuming that the ID is not displayed but kept for internal tracking
            self.report_table.item(row_position, 0).setData(Qt.UserRole, id)

            # Add export button to the table
            btn_export = PyTableButton("Export")
            btn_export.setFixedSize(75, 20)
            btn_export.clicked.connect(lambda *_: self.export_report(row_position))

            # 버튼을 중앙에 정렬하기 위한 새 위젯과 레이아웃 생성
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(btn_export)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            self.report_table.setCellWidget(row_position, 4, widget)

    def delete_report(self):
        selected_items = self.report_table.selectedItems()
        if not selected_items:
            print("선택된 리포트가 없습니다.")
            return
        row = selected_items[0].row()
        report_id = self.report_table.item(row, 0).data(Qt.UserRole)
        self.db_manager.delete_report_history(report_id)
        self.report_table.removeRow(row)

    def update_report_history(self):
        for row in range(self.report_table.rowCount()):
            report_id = self.report_table.item(row, 0).data(Qt.UserRole)
            template = self.report_table.item(row, 0).text()
            target = self.report_table.item(row, 1).text()
            date = self.report_table.item(row, 2).text()
            status = self.report_table.item(row, 3).text()
            self.db_manager.update_report_history(report_id, template, target, date, status)


    def export_report(self, row):
        template = self.report_table.item(row, 0).text()
        system_type = template.split('_')[0]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, f"{system_type}_template.xlsx")

        if not os.path.exists(template_path):
            print(f"Error: '{template_path}' does not exist.")
            return

        workbook = openpyxl.load_workbook(template_path)
        title_sheet = workbook['title']
        title_sheet['F21'].value = datetime.now().strftime('%Y-%m-%d')
        title_sheet['F21'].font = Font(size=14)

        static_sheet = workbook['statics']
        area_numbers = {'linux': ['1', '2', '3', '4', '5'], 'windows': ['1', '2', '3', '4', '5', '6'], 'database': ['1', '2', '3', '4', '5']}
        for area_no in area_numbers[system_type]:
            all_scores = self.db_manager.calculate_scores_for_all_ips(system_type, area_no)
            max_score = self.db_manager.calculate_max_scores(system_type)
            na_score = self.db_manager.calculate_na_severity_scores(system_type)
            row = int(area_no) + 2
            for severity, weight in [('상', 'C'), ('중', 'D'), ('하', 'E')]:
                static_sheet[f"{weight}{row}"] = all_scores.get(severity, 0)
            static_sheet[f"F{row}"] = max_score.get(area_no, 0)
            static_sheet[f"G{row}"] = na_score.get(area_no, 0)
            total_score = sum(all_scores.values())
            if max_score.get(area_no, 0) > na_score.get(area_no, 0):
                security_level = (total_score / (max_score.get(area_no, 0) - na_score.get(area_no, 0))) * 100
            else:
                security_level = 0
            static_sheet[f"H{row}"].number_format = '0%'  
            static_sheet[f"H{row}"] = security_level / 100 

        db_table = f"{system_type}_data"
        default_filename = f'{system_type}_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
        sheet_name = system_type
        sheet = workbook[sheet_name]
        ip_column_start = 5
        completed_ips = self.db_manager.fetch_completed_ips(db_table)
        for col_index, ip_tuple in enumerate(completed_ips, start=ip_column_start):
            ip = ip_tuple[0]
            ip_column = openpyxl.utils.get_column_letter(col_index)
            detail_data = self.db_manager.fetch_detail_data(db_table, ip)
            security_level = self.calculate_security_level(detail_data)
            sheet[f'{ip_column}{74 if system_type != "database" else 26}'].value = security_level
            db_table_modified = db_table.replace("_data", "")
            try:
                results = self.db_manager.fetch_check_results(f'{db_table_modified}_{ip.replace(".", "_")}')
            except Exception as e:
                print(f"Error fetching results for IP {ip}: {e}")
                continue
            sheet[f'{ip_column}1'].value = ip
            for index in range(2, 74 if system_type != "database" else 26):
                template_no = sheet[f'A{index}'].value
                db_result = next((res for res in results if res[0] == template_no), None)
                if db_result:
                    cell = sheet[f'{ip_column}{index}']
                    cell_value = "n/a" if db_result[1] == "n/a" else ("양호" if db_result[1] == "양호" else "취약")
                    cell.value = cell_value

        dialog_title = "Export Report"
        directory = os.path.join(current_dir, default_filename)
        file_filter = "Excel Workbook (*.xlsx)"
        selected_file, _ = QFileDialog.getSaveFileName(self, dialog_title, directory, file_filter)
        if selected_file:
            workbook.save(selected_file)
            self.report_table.setItem(row, 3, self.create_center_aligned_item("Completed"))


    def calculate_security_level(self, detail_data):
        total_score, max_score, na_score = 0, 0, 0
        severity_weights = {'상': 3, '중': 2, '하': 1}
        check_result_values = {'취약': 0, '양호': 1}

        for data in detail_data:
            severity, check_result = data[3], data[5]
            weight = severity_weights.get(severity, 0)
            max_score += weight

            if check_result != 'n/a':
                score = check_result_values.get(check_result, 0)
                total_score += weight * score
            else:
                na_score += weight

        max_score -= na_score
        security_level = (total_score / max_score) * 100 if max_score > 0 else 0
        return f"{round(security_level, 1)}%"

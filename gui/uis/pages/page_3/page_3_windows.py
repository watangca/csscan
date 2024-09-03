import os
import sys
import openpyxl
from qt_core import *
from gui.widgets import *
from datetime import datetime
from .windowschk import perform_windows_checks
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.database.DatabaseManager import DatabaseManager

# PyInstaller의 임시 폴더인 _MEIPASS를 고려하여 기본 경로 설정
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
additional_path = os.path.join(application_path)
if additional_path not in sys.path:
    sys.path.append(additional_path)


class Page3WindowsWidget(QWidget):
    windows_check_completed = Signal(str, str, str, str)

    def __init__(self):
        super().__init__()

        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

        self.detail_tab = QWidget()
        self.init_database()
        self.setup_ui()

    def init_database(self):
        self.db_manager = DatabaseManager()

    def setup_ui(self):
        # 메인 레이아웃 설정 
        self.main_layout = QVBoxLayout(self)

        # 탭 위젯 설정
        self.tabs = PyTab()
        self.check_tab = QWidget()
        self.result_tab = QWidget()

        # 탭 추가
        self.tabs.addTab(self.check_tab, "점검 수행")
        self.tabs.addTab(self.result_tab, "점검 결과")
        self.main_layout.addWidget(self.tabs)

        # 점검 수행 탭 레이아웃 설정
        self.check_layout = QVBoxLayout(self.check_tab)
        self.check_layout.setContentsMargins(0, 0, 0, 0)
        self.check_layout.setSpacing(10)

        # 상세 결과 탭 레이아웃 설정
        self.tabs.addTab(self.detail_tab, "상세 결과")
        self.detail_tab_layout = QVBoxLayout(self.detail_tab)
        self.detail_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.detail_tab_layout.setSpacing(10)        

        self.check_table = PyTableWidget()
        self.setup_check_table()
        self.check_layout.addWidget(self.check_table)

        # 점검 결과 탭 레이아웃 설정
        self.result_layout = QVBoxLayout(self.result_tab)
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        self.result_layout.setSpacing(10)

        self.result_table = PyTableWidget()
        self.setup_result_table()
        self.result_layout.addWidget(self.result_table)

    # 점검수행 탭 테이블 
    def setup_check_table(self):
        self.check_table.setColumnCount(5)
        self.check_table.setHorizontalHeaderLabels(["NO", "IP", "OS", "STATUS", "CHECK"])
        header = self.check_table.horizontalHeader()
        for i in range(self.check_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.load_windows_data()
   
    # 점검수행 탭 데이터 로딩함수 
    def load_windows_data(self):
        data = self.db_manager.fetch_all_data("windows_data")
        self.check_table.setRowCount(len(data))
        for row, record in enumerate(data):
            _, no, ip, os, status, check_date = record
            self.check_table.setItem(row, 0, QTableWidgetItem(str(no)))
            self.check_table.setItem(row, 1, QTableWidgetItem(ip))
            self.check_table.setItem(row, 2, QTableWidgetItem(os))
            self.check_table.setItem(row, 3, QTableWidgetItem(status))

            for i in range(4):
                item = self.check_table.item(row, i)
                item.setTextAlignment(Qt.AlignCenter)

            button_text = "COMPLETED" if check_date else "CHECK"
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)

            button = PyTableButton(text=button_text)
            button.setFixedSize(75, 20)
            layout.addWidget(button)

            if button_text in ["CHECK", "COMPLETED"]:
                button.clicked.connect(self.perform_check)

            self.check_table.setCellWidget(row, 4, widget)

    # 점검수행 테이블 내 CHECK 버튼 수행 함수
    def perform_check(self):
        try:
            clicked_btn = self.sender()

            if clicked_btn:
                # 이미 점검이 완료된 경우
                if clicked_btn.text() == "COMPLETED":
                    response_dialog = PyChoiceBox('재점검 확인', '이 IP에 대한 점검이 이미 완료되었습니다. 재점검하시겠습니까?')
                    response = response_dialog.exec()
                    if response != QDialog.Accepted:  
                        return

                # 선택된 행 정보 가져오기
                table_widget = clicked_btn.parent().parent().parent()
                index = table_widget.indexAt(clicked_btn.parent().pos())
                row = index.row()
                no_item = table_widget.item(row, 0)
                ip_address_item =table_widget.item(row, 1)
                ip_address = ip_address_item.text()
                os_item = table_widget.item(row, 2)
                os_name = os_item.text()

                # 사용자 정보 입력 다이얼로그
                dialog = PyAuth("사용자 정보 입력")
                if not dialog.exec():
                    return
                username = dialog.username_entry.text()
                password = dialog.password_entry.text()

                results = perform_windows_checks(ip_address, username, password)

                for result in results:
                    try:
                        self.db_manager.update_checklist("windows", result['no'], ip_address, result['detail'], result['result'])
                    except Exception as e:
                        print(f"Failed to update database for check {result['no']}: {e}")

                # 점검 완료 후 공통으로 수행할 작업
                last_check_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db_manager.update_check_date("windows_data", ip_address, last_check_date)
                self.load_completed_checks()
                self.load_windows_data() 

                # 점검 완료 메시지 팝업 표시 (반복문 외부)
                clicked_btn.setText("COMPLETED")
                completed_msg = PyDialog('점검 완료', f'IP {ip_address}에 대한 점검이 완료되었습니다.')
                completed_msg.exec()

        except Exception as e:
            print(f"Error: {e}")
            error_msg = PyDialog('오류 발생', f'점검 중 오류가 발생했습니다: {e}')
            error_msg.exec()


    # 점검수행이 완료되면 windows_data 에 점검결과를 업데이트 하는 함수
    def on_windows_check_completed(self, no, ip_address, check_detail, check_result):
        try:
            button_to_update = self.findChild(PyPushButton, f"checkButton_{ip_address}")
            if button_to_update:
                self.db_manager.update_checklist("windows", no, ip_address, check_detail, check_result)
                button_to_update.setText("COMPLETED")
            else:
                print(f"Error: Could not find button for IP {ip_address}")
            self.load_windows_data()
        except Exception as e:
            print(f"데이터베이스 업데이트 오류: {e}")

    # 점검결과 탭 테이블
    def setup_result_table(self):
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(["NO", "IP", "OS", "점검완료일", "상세결과 보기", "내보내기"])
        header = self.result_table.horizontalHeader()
        for i in range(self.result_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        self.load_completed_checks()

    # 완료된 점검 결과 로딩 함수
    def load_completed_checks(self):
        # 테이블의 기존 데이터를 초기화
        self.result_table.setRowCount(0)

        # 최신 점검 데이터 로드
        completed_checks = self.db_manager.fetch_completed_checks("windows_data") 
        for check in completed_checks:
            no, ip_address, os, check_date = check
            self.add_completed_check_to_result_table(no, ip_address, os, check_date)
        
    def add_completed_check_to_result_table(self, no, ip_address, os_name, check_date):
        # 결과 테이블에 새로운 행을 추가하는 로직
        row_count = self.result_table.rowCount()
        self.result_table.insertRow(row_count)

        # 각 열에 데이터를 추가하고, 중앙 정렬을 적용합니다.
        center_alignment = Qt.AlignCenter
        no_item = QTableWidgetItem(str(no))
        no_item.setTextAlignment(center_alignment)
        self.result_table.setItem(row_count, 0, no_item)

        ip_item = QTableWidgetItem(ip_address)
        ip_item.setTextAlignment(center_alignment)
        self.result_table.setItem(row_count, 1, ip_item)

        os_item = QTableWidgetItem(os_name)
        os_item.setTextAlignment(center_alignment)
        self.result_table.setItem(row_count, 2, os_item)

        check_date_item = QTableWidgetItem(check_date)
        check_date_item.setTextAlignment(center_alignment)
        self.result_table.setItem(row_count, 3, check_date_item)

        detail_btn_widget = QWidget()
        detail_btn_layout = QHBoxLayout(detail_btn_widget)
        detail_btn_layout.setAlignment(Qt.AlignCenter)
        detail_btn_layout.setContentsMargins(0, 0, 0, 0)
        
        detail_btn = PyTableButton("Detail View")
        detail_btn.setFixedSize(75, 20)
        detail_btn.setProperty("ip_address", ip_address)  
        detail_btn.clicked.connect(self.detail_view_clicked)
        detail_btn_layout.addWidget(detail_btn)

        self.result_table.setCellWidget(row_count, 4, detail_btn_widget)

        # Export 버튼을 중앙에 정렬하여 추가
        export_btn_widget = QWidget()
        export_btn_layout = QHBoxLayout(export_btn_widget)
        export_btn_layout.setAlignment(Qt.AlignCenter)
        export_btn_layout.setContentsMargins(0, 0, 0, 0)
        
        export_btn = PyTableButton("Export")
        export_btn.setFixedSize(75, 20)

        export_btn.clicked.connect(self.export_clicked)
        export_btn_layout.addWidget(export_btn)
        export_btn.setProperty("ip_address", ip_address)  

        self.result_table.setCellWidget(row_count, 5, export_btn_widget)

    def detail_view_clicked(self):
        clicked_btn = self.sender()
        ip_address = clicked_btn.property("ip_address")  

        if ip_address:
            self.show_result_detail(ip_address) 
    
    def export_clicked(self):
        clicked_btn = self.sender()
        ip_address = clicked_btn.property("ip_address")

        if not ip_address:
            PyDialog.warning(self, '경고', 'IP 주소가 없습니다.')
            return

        checklist_type = "windows"  
        result_detail_data = self.db_manager.fetch_detail_data(checklist_type, ip_address)  

        if not result_detail_data:
            PyDialog.warning(self, '경고', '상세 결과 데이터가 없습니다.')
            return

        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(current_dir, 'windows_detail.xlsx')
        workbook = openpyxl.load_workbook(template_path)
        
        sheet1 = workbook['점검 상세결과'] 
        sheet1['A1'] = ip_address 

        for index, (no, category, check_item, severity, detail_result, check_result) in enumerate(result_detail_data, start=3):
            sheet1[f'E{index}'] = detail_result 
            sheet1[f'F{index}'] = check_result  

        # Get the creation date for the filename
        creation_date = datetime.now().strftime('%Y%m%d')
        filename = f"{ip_address}_{creation_date}.xlsx"
        filepath = QFileDialog.getSaveFileName(self, "Save File", filename, "Excel Files (*.xlsx)")

        if filepath[0]:
            workbook.save(filepath[0])
            PyDialog.information(self, '알림', '파일이 저장되었습니다.')
        else:
            PyDialog.warning(self, '경고', '파일 저장이 취소되었습니다.')
       
    # 점검결과 탭 내 Detail view 클리시 테이블 상세결과 결과 
    def show_result_detail(self, ip_address):
        # 새 탭에 테이블 추가        
        checklist_type = "windows"  
        result_detail_data = self.db_manager.fetch_detail_data(checklist_type, ip_address)

        # 기존 테이블을 제거하고 새로운 테이블 생성
        self.clear_layout(self.detail_tab_layout)  # 기존 탭의 내용을 지우는 함수

        self.detail_table = PyTableWidget()
        self.detail_table.setColumnCount(6)
        self.detail_table.setHorizontalHeaderLabels(["NO", "카테고리", "점검항목", "심각도", "상세결과", "점검결과"])
        self.detail_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 가져온 데이터로 테이블 채우기
        self.detail_table.setRowCount(len(result_detail_data))
        for row, record in enumerate(result_detail_data):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                if col in [0, 3, 5]:
                    item.setTextAlignment(Qt.AlignCenter)
                self.detail_table.setItem(row, col, item)

        self.detail_tab_layout.addWidget(self.detail_table)
        self.tabs.setCurrentWidget(self.detail_tab)  # 상세 결과 탭으로 전환

    def clear_layout(self, layout):
        # 레이아웃 내의 모든 위젯을 제거하는 함수
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
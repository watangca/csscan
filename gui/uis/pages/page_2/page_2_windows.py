import os
import re
import socket
import platform 
import pandas as pd
from qt_core import *
from gui.widgets import *
from gui.database.DatabaseManager import DatabaseManager
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from login.license.licensemanager import determine_license_path, load_license_file


class Page2WindowsWidget(QWidget):
    dataChanged = Signal()


    def __init__(self, page3_widget=None):
        super().__init__()
        self.page3_widget = page3_widget
        self.db_manager = DatabaseManager()
        self.setup_ui()

        # 라이센스 파일 로딩
        license_dirname = "license"
        license_filename = "license.key"
        key_filename = "key.key"
        license_path, key_path = determine_license_path(license_dirname, license_filename, key_filename)
        license_info = load_license_file(license_path, key_path)
        
        if license_info:
            self.max_ip_count = license_info.get("windows_max_usage", 0)  # 원도우에 대한 최대 IP 개수 로드
        else:
            self.max_ip_count = 0  # 라이센스 로딩 실패 시 기본값 설정

        self.load_windows_data()

    def setup_ui(self):
        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

        self.init_layouts()
        self.init_windows_widgets()
        self.setLayout(self.main_layout)

    def init_layouts(self):
        self.main_layout = QVBoxLayout(self)

    def init_windows_widgets(self):
        layout = QHBoxLayout()

        self.windowsIpInput = PyLineEdit(place_holder_text="Enter windows server ip")
        layout.addWidget(self.windowsIpInput)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        self.registerButton = PyPushButton(text="등록")
        self.registerButton.clicked.connect(self.on_windows_register_clicked)
        layout.addWidget(self.registerButton)

        self.deleteButton = PyPushButton(text="삭제")
        self.deleteButton.clicked.connect(self.on_windows_delete_clicked)
        layout.addWidget(self.deleteButton)

        self.uploadButton = PyPushButton(text="업로드")
        self.uploadButton.clicked.connect(self.on_windows_upload_clicked)
        layout.addWidget(self.uploadButton)

        self.main_layout.addLayout(layout)

        self.windowsIpTableWidget = PyTableWidget()
        self.windowsIpTableWidget.setColumnCount(4)
        self.windowsIpTableWidget.setHorizontalHeaderLabels(["NO", "IP", "OS", "STATUS"])
        self.main_layout.addWidget(self.windowsIpTableWidget)
        for i in range(self.windowsIpTableWidget.columnCount()):
            self.windowsIpTableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)


    def set_item_centered(self, table_widget, row, col, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        table_widget.setItem(row, col, item)

    def load_data_to_table(self, data, table_widget):
        table_widget.setRowCount(0)
        for idx, row_data in enumerate(data, start=1):
            row_position = table_widget.rowCount()
            table_widget.insertRow(row_position)
            self.set_item_centered(table_widget, row_position, 0, str(idx))
            
            for col, item in enumerate(row_data[2:], start=1): 
                self.set_item_centered(table_widget, row_position, col, str(item))


    def on_windows_register_clicked(self):

        current_ip_count = self.db_manager.get_data_count("windows_data")

        if current_ip_count >= self.max_ip_count:
            PyDialog.warning(self, "라이센스 제한", f"최대 등록 가능한 IP 개수({self.max_ip_count}개)를 초과했습니다.")
            return
        
        ip = self.windowsIpInput.text()

        if not self.is_valid_ip(ip):
            PyDialog.warning(self, "유효하지 않은 IP", "올바른 IP 주소를 입력해주세요.")
            return
        
        ip_type = "windows"
        network_status = self.check_network(ip)

        row_position = self.windowsIpTableWidget.rowCount()
        self.windowsIpTableWidget.insertRow(row_position)
        self.set_item_centered(self.windowsIpTableWidget, row_position, 0, str(row_position + 1))
        self.set_item_centered(self.windowsIpTableWidget, row_position, 1, ip)
        self.set_item_centered(self.windowsIpTableWidget, row_position, 2, ip_type)
        self.set_item_centered(self.windowsIpTableWidget, row_position, 3, network_status)
        self.db_manager.save_single_data("windows_data", (ip, ip_type, network_status))
        self.load_windows_data() 
        self.update_page3_data()
        self.dataChanged.emit()

    def is_valid_ip(self, ip):
        # 정규 표현식을 사용하여 IP 주소의 유효성을 검사합니다.
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        return pattern.match(ip) is not None    

    def on_windows_delete_clicked(self):
        selected_rows = sorted(set(item.row() for item in self.windowsIpTableWidget.selectedItems()))
        for row in reversed(selected_rows):
            ip = self.windowsIpTableWidget.item(row, 1).text()
            # 테이블에서 IP 삭제
            self.db_manager.delete_single_data("windows_data", ip)
            # 관련 점검 결과 테이블도 삭제
            self.db_manager.delete_check_table_for_ip(ip, 'windows') 
            
        self.db_manager.renumber_no_column("windows_data")  # 데이터베이스의 NO 컬럼 재정렬
        self.load_windows_data()  # 업데이트된 데이터로 UI 재로딩
        self.update_page3_data()
        self.dataChanged.emit()

    def on_windows_upload_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            self.load_data_from_excel(file_name)
        self.update_page3_data()

    def update_page3_data(self):
        if self.page3_widget:
            self.page3_widget.load_windows_data()

    def load_data_from_excel(self, file_name):
        try:
            # 파일 읽기 시도
            data = pd.read_excel(file_name)
            for idx, row in data.iterrows():
                ip = row['IP']
                os_type = row['OS']
                status = self.check_network(ip)

                # 테이블에 데이터 추가
                row_position = self.windowsIpTableWidget.rowCount() + 1
                self.windowsIpTableWidget.insertRow(row_position - 1)
                self.set_item_centered(self.windowsIpTableWidget, row_position - 1, 0, str(row_position))
                self.set_item_centered(self.windowsIpTableWidget, row_position - 1, 1, ip)
                self.set_item_centered(self.windowsIpTableWidget, row_position - 1, 2, os_type)
                self.set_item_centered(self.windowsIpTableWidget, row_position - 1, 3, status)

                self.db_manager.save_single_data("windows_data", (ip, os_type, status))

            self.load_windows_data()
            self.dataChanged.emit()
        except Exception as e:
            # 오류 메시지 표시
            PyDialog.information(self, "오류", "올바른 엑셀 파일을 선택해주세요.\n" + str(e))   

    def load_windows_data(self):
        data = self.db_manager.fetch_all_data("windows_data")
        self.load_data_to_table(data, self.windowsIpTableWidget)

    def check_network(self, ip):
        # 운영 체제에 따라 적절한 ping 명령 실행
        if platform.system() == "Windows":
            response = os.system(f"ping -n 1 {ip}")
        else:
            response = os.system(f"ping -c 1 {ip}")

        if response != 0:
            return "Off"  # 핑 실패 시 "Off" 반환

        # 핑이 성공적이면 추가적으로 포트 5985 체크
        port = 5985  # Windows PowerShell Remoting 포트
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return "On"  # 포트가 열려 있으면 "On" 반환

        return "Off"
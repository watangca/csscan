from qt_core import *
from gui.widgets import *
from gui.database.DatabaseManager import DatabaseManager
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.uis.windows.main_window.functions_main_window import *

class Page1Widget(QWidget):
    def __init__(self):
        super().__init__()

        # DatabaseManager 인스턴스 생성
        self.database_manager = DatabaseManager()

        # UI 설정
        self.setup_ui()
        self.update_security_levels_and_ui()
        
    def setup_ui(self):
        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

        # 메인 수평 레이아웃
        main_layout = QHBoxLayout(self)

        linux_security_level = self.calculate_security_level("linux")
        windows_security_level = self.calculate_security_level("windows")
        database_security_level = self.calculate_security_level("database")

        # 리눅스 섹션 설정
        linux_layout = QVBoxLayout()
        self.linux_progress = PyCircularProgress(
            value = linux_security_level,
            progress_width=10,
            progress_color = self.themes["app_color"]["red"],
            text_color = self.themes["app_color"]["text_title"],
            font_size = 14,
            bg_color = self.themes["app_color"]["dark_four"]
        )
        self.linux_progress.setFixedSize(200, 200)
        self.linux_label = QLabel("Linux Security Level")
        linux_layout.addWidget(self.linux_progress, alignment=Qt.AlignCenter)  
        linux_layout.addSpacing(40)
        linux_layout.addWidget(self.linux_label, alignment=Qt.AlignCenter)  
        linux_layout.addSpacing(40)
        self.linux_table = PyTableWidget()
        self.linux_table.setColumnCount(2)
        self.linux_table.setHorizontalHeaderLabels(['리눅스 요약', '상세 결과'])
        self.linux_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        linux_layout.addWidget(self.linux_table)

        # 윈도우 섹션 설정
        windows_layout = QVBoxLayout()
        self.windows_progress = PyCircularProgress(
            value = windows_security_level,
            progress_width = 10,
            progress_color = self.themes["app_color"]["yellow"],
            text_color = self.themes["app_color"]["context_color"],
            font_size = 14,
            bg_color = self.themes["app_color"]["bg_three"]
        )
        self.windows_progress.setFixedSize(200, 200)
        self.windows_label = QLabel("Windows Security Level")
        windows_layout.addWidget(self.windows_progress, alignment=Qt.AlignCenter) 
        windows_layout.addSpacing(40)
        windows_layout.addWidget(self.windows_label, alignment=Qt.AlignCenter) 
        windows_layout.addSpacing(40)
        self.windows_table = PyTableWidget()
        self.windows_table.setColumnCount(2)
        self.windows_table.setHorizontalHeaderLabels(['윈도우 요약', '상세 결과'])
        self.windows_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        windows_layout.addWidget(self.windows_table)

        # 데이터베이스 섹션 설정
        database_layout = QVBoxLayout()
        self.database_progress = PyCircularProgress(
            value = database_security_level,
            progress_width = 10,
            progress_color = self.themes["app_color"]["blue"],
            text_color = self.themes["app_color"]["white"],
            font_size = 14,
            bg_color = self.themes["app_color"]["bg_three"]
        )
        self.database_progress.setFixedSize(200, 200)
        self.database_label = QLabel("Database Security Level")
        database_layout.addWidget(self.database_progress, alignment=Qt.AlignCenter) 
        database_layout.addSpacing(40)
        database_layout.addWidget(self.database_label, alignment=Qt.AlignCenter)  
        database_layout.addSpacing(40)
        self.database_table = PyTableWidget()
        self.database_table.setColumnCount(2)
        self.database_table.setHorizontalHeaderLabels(['데이터베이스 요약', '상세 결과'])
        self.database_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        database_layout.addWidget(self.database_table)

        # 각 섹션을 메인 레이아웃에 수평으로 추가
        main_layout.addLayout(linux_layout)
        main_layout.addLayout(windows_layout)
        main_layout.addLayout(database_layout)

        self.setLayout(main_layout)

        self.update_security_levels_and_ui()

        # 요약 정보를 테이블에 업데이트
        self.update_summary_tables()

    def calculate_security_level(self, system_type):
        completed_ips = self.database_manager.fetch_completed_ips(f"{system_type}_data")
        total_security_level = 0

        for ip in completed_ips:
            ip_address = ip[0]
            check_date = self.database_manager.fetch_check_date(f"{system_type}_data", ip_address)
            if check_date is None:
                continue  # 점검이 완료되지 않은 IP는 건너뜁니다.

            detail_data = self.database_manager.fetch_detail_data(system_type, ip_address)
            total_score = 0
            max_score = 0
            na_score = 0  # n/a 항목에 대한 점수
            severity_weights = {'상': 3, '중': 2, '하': 1}
            check_result_values = {'취약': 0, '양호': 1}

            for row in detail_data:
                severity = row[3]
                check_result = row[5]

                max_score += severity_weights[severity]
                if check_result == 'n/a':
                    na_score += severity_weights[severity]
                else:
                    total_score += severity_weights[severity] * check_result_values.get(check_result, 0)

            max_score -= na_score  # n/a 점수 제외
            security_level = (total_score / max_score) * 100 if max_score > 0 else 0
            total_security_level += security_level

        # 점검이 완료된 IP 주소의 수를 기준으로 평균 보안 수준을 계산합니다.
        completed_count = len([ip for ip in completed_ips if self.database_manager.fetch_check_date(f"{system_type}_data", ip[0]) is not None])
        average_security_level = total_security_level / completed_count if completed_count > 0 else 0
        
        return round(average_security_level, 1)

    
    def update_security_levels_and_ui(self):
        # 보안 수준 업데이트 코드를 여기서 실행
        linux_security_level = self.calculate_security_level("linux")
        windows_security_level = self.calculate_security_level("windows")
        database_security_level = self.calculate_security_level("database")

        self.linux_progress.set_value(linux_security_level)
        self.windows_progress.set_value(windows_security_level)
        self.database_progress.set_value(database_security_level)

        self.update_summary_tables()

    def generate_summary(self, system_type):
        completed_ips = [ip[0] for ip in self.database_manager.fetch_completed_ips(f"{system_type}_data")]
        vulnerability_count = self.database_manager.fetch_vulnerability_count_by_ip(system_type, completed_ips)
        high_count = self.database_manager.fetch_severity_count_by_ip(f"{system_type}_checklist", system_type, completed_ips, '상')
        medium_count = self.database_manager.fetch_severity_count_by_ip(f"{system_type}_checklist", system_type, completed_ips, '중')
        low_count = self.database_manager.fetch_severity_count_by_ip(f"{system_type}_checklist", system_type, completed_ips, '하')

        check_count = len(completed_ips)
        
        return {
            "check_count": check_count,
            "vulnerability_count": vulnerability_count,
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count
        }

    def update_summary_tables(self):
        # Linux 요약 정보
        linux_summary = self.generate_summary("linux")
        self.update_table_widget(self.linux_table, linux_summary)

        # Windows 요약 정보
        windows_summary = self.generate_summary("windows")
        self.update_table_widget(self.windows_table, windows_summary)

        # Database 요약 정보
        database_summary = self.generate_summary("database")
        self.update_table_widget(self.database_table, database_summary)


    def update_table_widget(self, table_widget, summary):
        # Clear previous data in the table
        table_widget.clearContents()
        table_widget.setRowCount(0)

        # Define the headers
        headers = ["점검 대수", "취약 건수", "HIGH 취약점 건수", "MEDIUM 취약점 건수", "LOW 취약점 건수"]
        data = [
            summary['check_count'],
            summary['vulnerability_count'],
            summary['high_count'],
            summary['medium_count'],
            summary['low_count']
        ]

        # Insert new data
        for i, header in enumerate(headers):
            row_position = table_widget.rowCount()
            table_widget.insertRow(row_position)
            item_header = QTableWidgetItem(header)
            item_data = QTableWidgetItem(str(data[i]))

            # Set text alignment to center
            item_header.setTextAlignment(Qt.AlignCenter)
            item_data.setTextAlignment(Qt.AlignCenter)

            table_widget.setItem(row_position, 0, item_header)
            table_widget.setItem(row_position, 1, item_data)




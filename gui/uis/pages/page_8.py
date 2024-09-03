from qt_core import *
from gui.widgets import *
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.database.DatabaseManager import DatabaseManager

class Page8Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

        self.db_manager = DatabaseManager()

        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

    def setup_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        # 검색 영역 설정
        search_layout = QHBoxLayout()
        self.system_type_combo = QComboBox()
        self.system_type_combo.addItems(["linux", "windows", "database"])
        self.ip_input = PyLineEdit()
        self.ip_input.setPlaceholderText("IP 입력")
        self.no_input = PyLineEdit()
        self.no_input.setPlaceholderText("No 입력")
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["상", "중", "하"])
        self.result_combo = QComboBox()
        self.result_combo.addItems(["양호", "취약", "n/a"])
        
        # 스페이서 추가
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # 검색 버튼 설정
        self.search_button = PyPushButton("검색")
        self.search_button.clicked.connect(self.on_search)

        # 검색 레이아웃에 위젯 및 스페이서 추가
        search_layout.addWidget(self.system_type_combo)
        search_layout.addWidget(self.ip_input)
        search_layout.addWidget(self.no_input)
        search_layout.addWidget(self.severity_combo)
        search_layout.addWidget(self.result_combo)
        search_layout.addItem(spacer)  # 스페이서 위치 조정
        search_layout.addWidget(self.search_button)
        
        # 메인 레이아웃에 검색 레이아웃 추가
        self.layout().addLayout(search_layout)

        # 결과 테이블 설정
        self.results_table = PyTableWidget()
        self.layout().addWidget(self.results_table)
        self.results_table.setColumnCount(7)  # 열의 수를 조정했습니다.
        self.results_table.setHorizontalHeaderLabels(["영역", "IP", "No", "Category", "Check List", "Severity", "Result"])
    
        # 초기에 결과 테이블을 숨깁니다.
        self.results_table.setVisible(False)

    def on_search(self):
        system_type = self.system_type_combo.currentText().lower()
        ip = self.ip_input.text()
        no = self.no_input.text() if self.no_input.text() else None
        severity = self.severity_combo.currentText()
        result = self.result_combo.currentText()
        
        # '전체' 선택 항목 처리
        no = None if no == "전체" else no
        severity = None if severity == "전체" else severity
        result = None if result == "전체" else result

        results = self.db_manager.search_inspection_results(system_type, ip, no, severity, result)
            
        # 결과가 있을 경우에만 테이블을 보이게 합니다.
        if results:
            self.update_results_table(results)
            self.results_table.setVisible(True)  # 검색 결과가 있으면 테이블을 보이게 합니다.
        else:
            self.results_table.setVisible(False)  # 검색 결과가 없으면 테이블을 숨깁니다.

    def update_results_table(self, results):
        # 테이블 설정
        self.results_table.setColumnCount(8)  # 열의 수를 8개로 설정
        self.results_table.setHorizontalHeaderLabels(["시스템 유형", "IP 주소", "번호", "카테고리", "점검 항목", "심각도", "결과", "점검 상세"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 모든 열을 테이블 너비에 맞게 조정

        # 테이블의 행 수를 검색 결과의 수에 맞게 조정
        self.results_table.setRowCount(len(results))

        # 검색 결과 데이터를 테이블에 채우기
        for row_index, row_data in enumerate(results):
            for column_index, data in enumerate(row_data):
                if column_index == 7:  # '점검 상세' 열
                    # 점검 상세 내용이 긴 경우 축약하여 표시
                    display_text = (str(data)[:50] + '...') if len(str(data)) > 50 else str(data)
                    item = QTableWidgetItem(display_text)
                    item.setToolTip(str(data))  # 전체 데이터를 툴팁으로 설정
                else:
                    item = QTableWidgetItem(str(data))
                if column_index in [0, 1, 2, 3,5, 6]:  # 중앙 정렬이 필요한 열 지정
                    item.setTextAlignment(Qt.AlignCenter)
                self.results_table.setItem(row_index, column_index, item)





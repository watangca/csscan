from qt_core import *
from gui.widgets.py_line_edit import PyLineEdit
from gui.widgets.py_push_button import PyPushButton
from gui.widgets.py_dialog import PyDialog

# 테마 데이터 직접 정의
theme_data = {
    "app_color": {
        "dark_one": "#1b1e23",
        "dark_two": "#1e2229",
        "dark_three": "#21252d",
        "dark_four": "#272c36",
        "bg_one": "#2c313c",
        "bg_two": "#343b48",
        "bg_three": "#3c4454",
        "icon_color": "#c3ccdf",
        "icon_hover": "#dce1ec",
        "icon_pressed": "#6c99f4",
        "icon_active": "#f5f6f9",
        "context_color": "#568af2",
        "context_hover": "#6c99f4",
        "context_pressed": "#3f6fd1",
        "text_title": "#dce1ec",
        "text_foreground": "#8a95aa",
        "text_description": "#4f5b6e",
        "text_active": "#dce1ec",
        "white": "#f5f6f9",
        "pink": "#ff007f",
        "green": "#00ff7f",
        "red": "#ff5555",
        "yellow": "#f1fa8c"
    }
}

class PyReportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.report_info = None  
        self.setup_ui()
        self.set_title("리포트 생성")
        self.apply_styles()

    def set_title(self, title):
        self.setWindowTitle(title)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 리포트 템플릿 드롭다운 메뉴
        self.template_label = QLabel("리포트 템플릿")
        self.template_dropdown = QComboBox()
        self.template_dropdown.addItems(["linux_template.xlsx","windows_template.xlsx", "database_template.xlsx"])
        layout.addWidget(self.template_label)
        layout.addWidget(self.template_dropdown)

        self.template_dropdown.currentIndexChanged.connect(self.on_template_change)

        # 리포팅 대상 드롭다운 메뉴
        self.target_label = QLabel("리포팅 대상")
        self.target_dropdown = QComboBox()
        self.target_dropdown.addItems(["linux", "windows", "database"])
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_dropdown)

        # 확인 및 취소 버튼
        self.submit_button = PyPushButton("확인")
        self.cancel_button = PyPushButton("취소")
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # 신호 연결
        self.submit_button.clicked.connect(self.submit)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def on_template_change(self, index):
        # 템플릿에 따라 리포팅 대상을 자동 설정
        template_to_target = {
            "windows_template.xlsx": "windows",
            "linux_template.xlsx": "linux",
            "database_template.xlsx": "database"
        }
        selected_template = self.template_dropdown.currentText()
        target = template_to_target.get(selected_template, "")
        if target:
            # 리포팅 대상 콤보박스에서 해당 값을 찾아서 설정
            target_index = self.target_dropdown.findText(target)
            if target_index >= 0:
                self.target_dropdown.setCurrentIndex(target_index)

    def submit(self):
        # 선택된 리포트 정보를 저장
        self.report_info = {
            "template": self.template_dropdown.currentText(),
            "target": self.target_dropdown.currentText()
        }
        self.accept()

    def get_report_info(self):
        # 저장된 리포트 정보를 반환하는 메서드
        return self.report_info

    def apply_styles(self):
        app_color = theme_data["app_color"]
        # Modify your style sheet as needed for the dialog
        self.setStyleSheet("""
        QDialog {{
            background-color: {bg_three};
            border-radius: 5px;
        }}
        QLabel {{
            font-size: 9pt;
            color: white;
        }}
        QComboBox {{
            font-size: 9pt;
        }}
        QPushButton {{
            font-size: 9pt;
        }}
        """.format(**app_color))
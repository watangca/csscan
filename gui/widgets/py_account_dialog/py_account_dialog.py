from qt_core import *
from gui.widgets.py_line_edit import PyLineEdit
from gui.widgets.py_push_button import PyPushButton
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyAccountDialog(QDialog):
    def __init__(self, title="", mode="add", account_data=None):
        super().__init__()
        self.mode = mode
        self.account_data = account_data if account_data else {}
        self.setup_ui()
        self.set_title(title)
        self.apply_styles()

    def set_title(self, title):
        if self.mode == "add":
            title = "계정 등록"
        elif self.mode == "edit":
            title = "계정 편집"
        elif self.mode == "delete":
            title = "계정 삭제"
        self.setWindowTitle(title)

    def setup_ui(self):
        layout = QVBoxLayout()

        # 사용자명, 이메일, 역할 입력 필드
        self.username_entry = PyLineEdit("사용자명")
        self.email_entry = PyLineEdit("이메일")
        self.role_entry = PyLineEdit("역할")
        layout.addWidget(self.username_entry)
        layout.addWidget(self.email_entry)
        layout.addWidget(self.role_entry)

        # 비밀번호 입력 필드 (모든 모드에서 사용)
        self.password_entry = PyLineEdit("비밀번호")
        layout.addWidget(self.password_entry)

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

        # 데이터 채우기
        if self.mode != "add" and self.account_data:
            self.fill_data()

        self.setLayout(layout)

    def fill_data(self):
        self.username_entry.setText(self.account_data.get("username", ""))
        self.email_entry.setText(self.account_data.get("email", ""))
        self.role_entry.setText(self.account_data.get("role", ""))
        # 비밀번호 필드는 삭제 모드에서 플레이스홀더 텍스트로 설정
        if self.mode == "delete":
            self.password_entry.setPlaceholderText("비밀번호 확인 필요")

    def submit(self):
        account_info = {
            "username": self.username_entry.text(),
            "email": self.email_entry.text(),
            "role": self.role_entry.text(),
            "password": self.password_entry.text()
        }
        self.accept()

    def apply_styles(self):

        self.setStyleSheet(f"""
        QDialog {{
            background-color: {theme_data['bg_three']};
            border-radius: 5px;
            min-width: 300px;
            max-width: 300px;
            min-height: 300px;
            max-height: 300px;
        }}
        QLineEdit {{
            font-size: 9pt;
        }}
        QPushButton {{
            font-size: 9pt;
        }}
        """)
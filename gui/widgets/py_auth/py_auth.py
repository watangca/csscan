from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyAuth(QDialog):
    def __init__(self, title="", *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 타이틀 설정
        if title:
            self.setWindowTitle(title)
        
        self.setFixedSize(250, 280)

        # 대화 상자 배경색 설정
        self.setStyleSheet(f"background-color: {theme_data['bg_three']};")

        # 레이아웃 생성
        layout = QVBoxLayout()

        # 사용자명 입력란
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("ID")
        self.username_entry.setStyleSheet(self.generate_line_edit_style())

        # 비밀번호 입력란
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("PW")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet(self.generate_line_edit_style())

        # 확인 버튼
        self.button = QPushButton("확인")
        self.button.setStyleSheet(self.generate_button_style())
        self.button.setFixedHeight(30)
        self.button.clicked.connect(self.accept)

        # 위젯을 레이아웃에 추가
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def generate_line_edit_style(self):
        return '''
        QLineEdit {{
            border-radius: 8px;
            border: 2px solid transparent;
            padding: 5px 5px;
            color: {text_foreground};
            background-color: {bg_two};
            selection-color: {white};
            selection-background-color: {context_color};
            font-size: 9px;  /* 플레이스홀더와 텍스트 폰트 크기 설정 */
        }}
        QLineEdit:focus {{
            background-color: {bg_one};
            border: 2px solid {context_color};
        }}
        QLineEdit::placeholder {{
            color: {placeholder_color};
            font-size: 9px;  /* 플레이스홀더 폰트 크기 설정 */
        }}
        '''.format(
            text_foreground=theme_data['text_foreground'],
            bg_two=theme_data['bg_two'],
            white=theme_data['white'],
            context_color=theme_data['context_color'],
            bg_one=theme_data['bg_one'],
            placeholder_color=theme_data['text_description'] 
        )

    def generate_button_style(self):
        return '''
        QPushButton {{
            background-color: {dark_one};
            color: {text_active};
            border-radius: 7px;
            border: none;
            font-size: 9px;
        }}
        QPushButton:checked, QPushButton:hover {{
            background-color: {context_color};
        }}
        QPushButton:pressed {{
            background-color: {context_pressed};
        }}
        '''.format(
            dark_one=theme_data['dark_one'],
            text_active=theme_data['text_active'],
            context_color=theme_data['context_color'],
            context_pressed=theme_data['context_pressed']
        )


class PyOracleAuth(PyAuth):
    def __init__(self, title=""):
        super().__init__(title)

        # Oracle 사용자 입력란
        self.oracle_user_entry = QLineEdit()
        self.oracle_user_entry.setPlaceholderText("Oracle User")
        self.oracle_user_entry.setStyleSheet(self.generate_line_edit_style())

        # Oracle 비밀번호 입력란
        self.oracle_password_entry = QLineEdit()
        self.oracle_password_entry.setPlaceholderText("Oracle Password")
        self.oracle_password_entry.setEchoMode(QLineEdit.Password)
        self.oracle_password_entry.setStyleSheet(self.generate_line_edit_style())

        # Oracle DSN 입력란
        self.oracle_dsn_entry = QLineEdit()
        self.oracle_dsn_entry.setPlaceholderText("Oracle DSN")
        self.oracle_dsn_entry.setStyleSheet(self.generate_line_edit_style())

        # 위젯을 레이아웃에 추가
        self.layout().insertWidget(2, self.oracle_user_entry)
        self.layout().insertWidget(3, self.oracle_password_entry)
        self.layout().insertWidget(4, self.oracle_dsn_entry)

class PyMySQLAuth(PyAuth):
    def __init__(self, title="MySQL Authentication"):
        super().__init__(title)

        # MySQL 사용자명 입력란
        self.mysql_user_entry = QLineEdit()
        self.mysql_user_entry.setPlaceholderText("MySQL Username")
        self.mysql_user_entry.setStyleSheet(self.generate_line_edit_style())

        # MySQL 비밀번호 입력란
        self.mysql_password_entry = QLineEdit()
        self.mysql_password_entry.setPlaceholderText("MySQL Password")
        self.mysql_password_entry.setEchoMode(QLineEdit.Password)
        self.mysql_password_entry.setStyleSheet(self.generate_line_edit_style())

        # MySQL 데이터베이스 이름 입력란
        self.mysql_db_entry = QLineEdit()
        self.mysql_db_entry.setPlaceholderText("MySQL Database")
        self.mysql_db_entry.setStyleSheet(self.generate_line_edit_style())

        # 위젯을 레이아웃에 추가
        self.layout().insertWidget(2, self.mysql_user_entry)
        self.layout().insertWidget(3, self.mysql_password_entry)
        self.layout().insertWidget(4, self.mysql_db_entry)

class PyMSSQLAuth(PyAuth):
    def __init__(self, title=""):
        super().__init__(title)  # 상위 클래스의 생성자 호출

        # MSSQL 데이터베이스 이름 입력란 추가
        self.mssql_db_entry = QLineEdit()
        self.mssql_db_entry.setPlaceholderText("MSSQL Database")
        self.mssql_db_entry.setStyleSheet(self.generate_line_edit_style())  # 상위 클래스의 스타일 메서드 사용
        self.layout().insertWidget(2, self.mssql_db_entry)

        # Windows 사용자명 입력란 추가
        self.windows_username_entry = QLineEdit()
        self.windows_username_entry.setPlaceholderText("Windows User")
        self.windows_username_entry.setStyleSheet(self.generate_line_edit_style())
        self.layout().insertWidget(3, self.windows_username_entry)

        # Windows 비밀번호 입력란 추가
        self.windows_password_entry = QLineEdit()
        self.windows_password_entry.setPlaceholderText("Windows Password")
        self.windows_password_entry.setEchoMode(QLineEdit.Password)
        self.windows_password_entry.setStyleSheet(self.generate_line_edit_style())
        self.layout().insertWidget(4, self.windows_password_entry)

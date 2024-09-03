from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']


class PyMessageBox(QDialog):
    def __init__(self, title, message, buttons=('OK',), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(title)
        self.setup_ui(message, buttons)

    def setup_ui(self, message, buttons):
        layout = QVBoxLayout()

        # 메시지 라벨 스타일 업데이트
        self.message_label = QLabel(message)
        self.message_label.setStyleSheet(f"color: {theme_data['text_foreground']}; font-size: 12px;")
        layout.addWidget(self.message_label)

        # 버튼 박스
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setCenterButtons(True)  # 버튼을 중앙에 배치
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme_data['context_color']};
                    color: {theme_data['white']};
                    border-radius: 5px;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {theme_data['context_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {theme_data['context_pressed']};
                }}
            """)
            self.buttonBox.addButton(button, QDialogButtonBox.ActionRole)
        self.buttonBox.clicked.connect(self.button_clicked)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

        # 대화 상자 스타일 업데이트
        self.setStyleSheet(f"""
        QDialog {{
            background-color: {theme_data['bg_one']};
            border-radius: 10px;
        }}
        """)

    def button_clicked(self, button):
        # 버튼의 텍스트에 따라 결과 설정
        button_text = button.text()
        if button_text == 'OK':
            self.setResult(QDialog.Accepted)
        elif button_text == 'Yes':
            self.setResult(QDialog.Accepted)
        elif button_text == 'No':
            self.setResult(QDialog.Rejected)
        else:
            # 기본 동작
            self.setResult(QDialog.Rejected)

        self.accept()
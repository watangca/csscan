from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyChoiceBox(QDialog):
    def __init__(self, title, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(title)
        self.setup_ui(message)
        self.apply_styles()

    def setup_ui(self, message):
        layout = QVBoxLayout()
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def apply_styles(self):
        global theme_data  # 전역 변수 theme_data 사용을 명시합니다.

        self.message_label.setStyleSheet(f"color: {theme_data['text_foreground']}; font-size: 10px;")
        self.buttonBox.setStyleSheet(f"""
        QDialogButtonBox QPushButton {{
            background-color: {theme_data['dark_one']};
            color: white;
            font-size: 9px;
            border-radius: 5px;
            padding: 5px;
            border: none;
            min-width: 70px;
            height: 20px;
        }}
        QDialogButtonBox QPushButton:hover {{
            background-color: {theme_data['context_pressed']};
        }}
        QDialogButtonBox QPushButton:pressed {{
            background-color: {theme_data['context_pressed']};
        }}
        """)
        self.setStyleSheet(f"""
        QDialog {{
            background-color: {theme_data['bg_three']};
            border-radius: 5px;
        }}
        """)




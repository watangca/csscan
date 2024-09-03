from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyDialog(QDialog):
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

        # OK 버튼
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def apply_styles(self):

        self.message_label.setStyleSheet(f"color: {theme_data['text_foreground']}; font-size: 9px;")
        self.buttonBox.setStyleSheet(f"""
        QDialogButtonBox QPushButton {{
            background-color: {theme_data['dark_one']};
            color: white;
            border-radius: 5px;
            padding: 5px;
            border: none;
            min-width: 70px;
            height: 20px;
            font-size: 9px;
        }}
        QDialogButtonBox QPushButton:hover {{
            background-color: {theme_data['context_pressed']};
            color: {theme_data['white']};
            font-size: 9px;
        }}
        """)
        self.setStyleSheet(f"""
        QDialog {{
            background-color: {theme_data['bg_three']};
            border-radius: 5px;
            font-size: 9px;
        }}
        """)

    @classmethod
    def warning(cls, parent, title, message):
        msgBox = cls(title, message, parent)
        msgBox.exec()
    
    @classmethod
    def information(cls, parent, title, message):
        msgBox = cls(title, message, parent)
        msgBox.exec()

from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']


class PyTableButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 스타일시트 설정
        self.setStyleSheet(f"""
        QPushButton {{
            background-color: {theme_data['dark_two']};
            color: {theme_data['text_title']};
            border-radius: 5px;
            border: none;
            font-size: 8px;
        }}
        QPushButton:checked, QPushButton:hover {{
            background-color: {theme_data['context_pressed']};
        }}
        QPushButton:pressed {{
            background-color: {theme_data['context_pressed']};
        }}
        """)

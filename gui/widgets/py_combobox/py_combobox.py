from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyComboBox(QComboBox):
    def __init__(self):
        super().__init__()

        # 스타일 적용
        self.apply_theme_style()

    def apply_theme_style(self):

        # 스타일시트 적용
        self.setStyleSheet(f'''
        QComboBox {{
            background-color: {theme_data['bg_two']};
            border-radius: 8px;
            padding: 5px;
            color: {theme_data['text_foreground']};
            min-width: 120px;
            min-height: 18px;
        }}
        QComboBox:hover {{
            border: 2px solid {theme_data['context_hover']};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: none;
            border-left-style: solid;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            background-color: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {theme_data['bg_two']};
            selection-background-color: {theme_data['context_hover']};
            selection-color: {theme_data['white']};
        }}
        ''')
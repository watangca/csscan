from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyPushButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__()

        self.setText(text)
        if parent is not None:
            self.setParent(parent)

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(80, 30)

        # 스타일 적용
        self.apply_theme_style()

    def apply_theme_style(self):

        # 스타일시트 생성
        stylesheet = f'''
        QPushButton {{
            border: none;
            padding-left: 10px;
            padding-right: 5px;
            color: {theme_data['text_title']};
            border-radius: 8px;
            background-color: {theme_data['dark_two']};
        }}
        QPushButton:hover {{
            background-color: {theme_data['context_pressed']};
            color: {theme_data['white']};
        }}
        QPushButton:pressed {{
            background-color: {theme_data['context_pressed']};
        }}
        '''

        # 스타일시트 적용
        self.setStyleSheet(stylesheet)

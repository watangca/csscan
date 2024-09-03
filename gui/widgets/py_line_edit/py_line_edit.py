from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyLineEdit(QLineEdit):
    # 클래스 변수로 스타일시트 설정
    base_style = f'''
        QLineEdit {{
            background-color: {theme_data['bg_two']};
            border-radius: 8px;
            border: 2px solid transparent;
            padding: 5px 5px;
            selection-color: {theme_data['context_color']};
            selection-background-color: {theme_data['icon_hover']};
            color: {theme_data['text_foreground']};
        }}
        QLineEdit:focus {{
            border: 2px solid {theme_data['context_color']};
            background-color: {theme_data['bg_one']};
        }}
    '''

    def __init__(self, place_holder_text=""):
        super().__init__()

        # Placeholder 텍스트 설정
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        # 스타일 적용
        self.apply_theme_style()

    def apply_theme_style(self):
        # 스타일시트 설정
        self.setStyleSheet(self.base_style)

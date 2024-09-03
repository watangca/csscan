from qt_core import *
from gui.core.json_themes import Themes

themes = Themes()
theme_data = themes.items['app_color']

class PyTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        # 기본 설정 적용
        self.set_default_settings()

        # 스타일 적용
        self.apply_theme_style()
    
    def set_default_settings(self):
        # 그리드 라인 숨기기
        self.setShowGrid(False)
        # 수직 헤더 숨기기
        self.verticalHeader().setVisible(False)

    def adjust_column_width_to_content(self):
        # 열 너비를 내용에 맞게 조절
        self.resizeColumnsToContents()

    def apply_theme_style(self):

        # 스타일시트 적용
        self.setStyleSheet(f'''
        /* QTableWidget */
        QTableWidget {{ 
            background-color: {theme_data['bg_two']};
            padding: 5px;
            border-radius: 8px;
            gridline-color: {theme_data['bg_one']};
            color: {theme_data['text_foreground']};
        }}
        QTableWidget::item {{
            border-color: none;
            padding-left: 5px;
            padding-right: 5px;
            gridline-color: {theme_data['bg_one']};
            border-bottom: 1px solid {theme_data['bg_three']};
        }}
        QTableWidget::item:selected {{
            background-color: {theme_data['context_color']};
        }}
        QHeaderView::section {{
            background-color: {theme_data['dark_three']};
            border: none;
            padding: 3px;
            border-bottom: none; /* 헤더의 새로운 선 제거 */
        }}
        QTableWidget::horizontalHeader {{   
            background-color: {theme_data['dark_two']};
            border-bottom: none; /* 헤더 하단 선 제거 */
        }}
        QTableWidget QTableCornerButton::section {{
            background-color: {theme_data['bg_two']};
        }}
        QHeaderView::section:horizontal {{
            background-color: {theme_data['dark_two']};
        }}
        QHeaderView::section:vertical {{
            background-color: {theme_data['bg_three']};
        }}
        QScrollBar:horizontal {{
            background: {theme_data['bg_one']};
            height: 6px; /* 수평 스크롤바 두께 조정 */
            margin: 0px 21px 0 21px;
            border-radius: 3px;
        }}
        QScrollBar::handle:horizontal {{
            background: {theme_data['context_color']};
            border-radius: 3px;
        }}
        QScrollBar:vertical {{
            background: {theme_data['bg_one']};
            width: 6px; /* 수직 스크롤바 두께 조정 */
            margin: 21px 0 21px 0;
            border-radius: 3px;
        }}
        QScrollBar::handle:vertical {{  
            background: {theme_data['context_color']};
            border-radius: 3px;
        }}
        /* 스크롤바 화살표 제거 */
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal,
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            width: 0px;
            height: 0px;
            background: none;
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            background: none;
            border: none;
        }}
        ''')
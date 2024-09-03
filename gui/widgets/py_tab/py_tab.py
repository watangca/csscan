from qt_core import *

# 테마 데이터 직접 정의
theme_data = {
    "app_color": {
        "dark_one": "#1b1e23",
        "dark_two": "#1e2229",
        "dark_three": "#21252d",
        "dark_four": "#272c36",
        "bg_one": "#2c313c",
        "bg_two": "#343b48",
        "bg_three": "#3c4454",
        "icon_color": "#c3ccdf",
        "icon_hover": "#dce1ec",
        "icon_pressed": "#6c99f4",
        "icon_active": "#f5f6f9",
        "context_color": "#568af2",
        "context_hover": "#6c99f4",
        "context_pressed": "#3f6fd1",
        "text_title": "#dce1ec",
        "text_foreground": "#8a95aa",
        "text_description": "#4f5b6e",
        "text_active": "#dce1ec",
        "white": "#f5f6f9",
        "pink": "#ff007f",
        "green": "#00ff7f",
        "red": "#ff5555",
        "yellow": "#f1fa8c"
    }
}

class PyTab(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tab_height = "15px"

        # 스타일시트 설정
        self.setStyleSheet(f"""
        QTabWidget::pane {{
            border: 0;
            background: {theme_data['app_color']['dark_three']};
            border-radius: 5px;
            padding: 0;
        }}
        QTabWidget::tab-bar {{
            left: 0px;
        }}
        QTabBar::tab {{
            background: {theme_data['app_color']['dark_four']};
            color: {theme_data['app_color']['text_description']};
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 5px;
            min-width: 80px;
            min-height: {tab_height}; 
        }}
        QTabBar::tab:hover {{
            background: {theme_data['app_color']['context_hover']};
        }}
        QTabBar::tab:selected {{
            background: {theme_data['app_color']['context_pressed']};
            color: {theme_data['app_color']['text_title']};
        }}
        QTabBar::tab:!selected {{
            margin-top: 0px;
            background: {theme_data['app_color']['dark_one']}; 
            color: {theme_data['app_color']['text_foreground']};
        }}
        """)

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

class PyResetButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        # Access colors from theme_data
        button_text_color = theme_data['app_color']['text_foreground']
        button_hover_color = theme_data['app_color']['icon_hover']
        button_padding = "5px"  
        
        # Update the style sheet with theme colors
        self.setStyleSheet(f"""
        QPushButton {{
            background-color: transparent;
            color: {button_text_color};
            border: none;
            text-decoration: underline;
            padding: {button_padding};
        }}
        QPushButton:hover {{
            color: {button_hover_color};
        }}
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))

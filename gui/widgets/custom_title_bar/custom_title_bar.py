from qt_core import *
from gui.core.json_themes import Themes
from gui.core.functions import *

themes = Themes()
theme_data = themes.items['app_color']


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.theme_data = theme_data

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 제목 라벨
        self.titleLabel = QLabel("")
        self.titleLabel.setFixedHeight(30)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet(f"""
            background-color: {self.theme_data['dark_two']};
            color: {self.theme_data['text_title']};
            font-size: 10pt;
        """)

        # 버튼 초기화 및 설정
        self.minimizeButton = QPushButton()
        self.closeButton = QPushButton()

        # 버튼에 아이콘 및 스타일 적용
        self.setIconToButton(self.minimizeButton, "icon_minimize.svg")
        self.setStyleToButton(self.minimizeButton)
        self.setIconToButton(self.closeButton, "icon_close.svg")
        self.setStyleToButton(self.closeButton, isCloseButton=True)

        # 레이아웃에 위젯 추가
        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.minimizeButton)
        self.layout.addWidget(self.closeButton)
        self.setLayout(self.layout)

        # 마우스 이벤트를 위한 변수
        self.start = QPoint(0, 0)
        self.pressing = False

    def setIconToButton(self, button, icon_name):
        # SVG 아이콘 경로 설정
        icon_path = Functions.set_svg_icon(icon_name)
        
        # 아이콘 설정
        button.setIcon(QIcon(icon_path))

        # 아이콘 크기 설정
        button.setIconSize(QSize(15, 15))

    def setStyleToButton(self, button, isCloseButton=False):
        button.setFixedSize(QSize(30, 30))
        if button == self.minimizeButton:
            button.clicked.connect(self.minimizeWindow)
        elif button == self.closeButton:
            button.clicked.connect(self.closeWindow)

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.theme_data['dark_three']};
                color: {self.theme_data['icon_color']};
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.theme_data['dark_four']};
            }}
            QPushButton:pressed {{
                background-color: {self.theme_data['bg_three']};
            }}
        """)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    # 마우스 이동 이벤트 처리
    def mouseMoveEvent(self, event):
        if self.pressing:
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.move(self.parent.pos() + movement)
            self.start = end
        
    def minimizeWindow(self):
        self.parent.showMinimized()

    def closeWindow(self):
        self.parent.close()



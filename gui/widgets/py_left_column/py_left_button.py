# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# PY TITLE BUTTON
# ///////////////////////////////////////////////////////////////
class PyLeftButton(QPushButton):
    def __init__(
        self,
        parent,
        app_parent = None,
        tooltip_text = "",
        btn_id = None,
        width = 30,
        height = 30,
        radius = 8,
        bg_color = "#343b48",
        bg_color_hover = "#3c4454",
        bg_color_pressed = "#2c313c",
        icon_color = "#c3ccdf",
        icon_color_hover = "#dce1ec",
        icon_color_pressed = "#edf0f5",
        icon_color_active = "#f5f6f9",
        icon_path = "no_icon.svg",
        dark_one = "#1b1e23",
        context_color = "#568af2",
        text_foreground = "#8a95aa",
        is_active = False
    ):
        super().__init__()
        self.icon_cache = {}
        
        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName(btn_id)

        # PROPERTIES
        self._bg_color = bg_color
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed        
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._top_margin = self.height() + 6
        self._is_active = is_active
        # Set Parameters
        self._set_bg_color = bg_color
        self._set_icon_path = icon_path
        self._set_icon_color = icon_color
        self._set_border_radius = radius
        # Parent
        self._parent = parent
        self._app_parent = app_parent

        # TOOLTIP
        self._tooltip_text = tooltip_text
        self._tooltip = _ToolTip(
            app_parent,
            tooltip_text,
            dark_one,
            context_color,
            text_foreground
        )
        self._tooltip.hide()

    # SET ACTIVE MENU
    # ///////////////////////////////////////////////////////////////
    def set_active(self, is_active):
        self._is_active = is_active
        self.update()

    # RETURN IF IS ACTIVE MENU
    # ///////////////////////////////////////////////////////////////
    def is_active(self):
        return self._is_active

    # PAINT EVENT
    # painting the button and the icon
    # ///////////////////////////////////////////////////////////////
    def paintEvent(self, event):
        # PAINTER
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self._is_active:
            # BRUSH
            brush = QBrush(QColor(self._bg_color_pressed))
        else:
            # BRUSH
            brush = QBrush(QColor(self._set_bg_color))

        # CREATE RECTANGLE
        rect = QRect(0, 0, self.width(), self.height())
        paint.setPen(Qt.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(
            rect, 
            self._set_border_radius, 
            self._set_border_radius
        )

        # DRAW ICONS
        self.icon_paint(paint, self._set_icon_path, rect)

        # END PAINTER
        paint.end()

    # CHANGE STYLES
    # Functions with custom styles
    # ///////////////////////////////////////////////////////////////
    def change_style(self, event):
        if event == QEvent.Enter:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.update()         
        elif event == QEvent.Leave:
            self._set_bg_color = self._bg_color
            self._set_icon_color = self._icon_color
            self.update()
        elif event == QEvent.MouseButtonPress:            
            self._set_bg_color = self._bg_color_pressed
            self._set_icon_color = self._icon_color_pressed
            self.update()
        elif event == QEvent.MouseButtonRelease:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.update()

    # MOUSE OVER
    # Event triggered when the mouse is over the BTN
    # ///////////////////////////////////////////////////////////////
    def enterEvent(self, event):
        self.change_style(QEvent.Enter)
        self.move_tooltip()
        self._tooltip.show()

    # MOUSE LEAVE
    # Event fired when the mouse leaves the BTN
    # ///////////////////////////////////////////////////////////////
    def leaveEvent(self, event):
        self.change_style(QEvent.Leave)
        self.move_tooltip()
        self._tooltip.hide()

    # MOUSE PRESS
    # Event triggered when the left button is pressed
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonPress)
            # SET FOCUS
            self.setFocus()
            # EMIT SIGNAL
            return self.clicked.emit()

    # MOUSE RELEASED
    # Event triggered after the mouse button is released
    # ///////////////////////////////////////////////////////////////
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.change_style(QEvent.MouseButtonRelease)
            # EMIT SIGNAL
            return self.released.emit()

    # DRAW ICON WITH COLORS
    # ///////////////////////////////////////////////////////////////
    def update_icon(self, image):
        if image not in self.icon_cache:
            self.icon_cache[image] = QPixmap(image)

    def icon_paint(self, qp, image, rect):
        # QPixmap 객체 캐싱 및 로드
        if image not in self.icon_cache:
            self.icon_cache[image] = QPixmap(image)
        icon = self.icon_cache[image]

        # 현재 QPixmap의 색상과 변경하려는 색상 비교
        current_color = icon.cache_color if hasattr(icon, 'cache_color') else None
        new_color = self._context_color if self._is_active else self._set_icon_color

        # 색상 변경이 필요한 경우에만 QPainter 사용
        if current_color != new_color:
            painter = QPainter(icon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(icon.rect(), new_color)
            painter.end()
            icon.cache_color = new_color  # 색상 캐시 업데이트

        # QPixmap 그리기
        x = (rect.width() - icon.width()) / 2
        y = (rect.height() - icon.height()) / 2
        qp.drawPixmap(x, y, icon)

    # SET ICON
    # ///////////////////////////////////////////////////////////////
    def set_icon(self, icon_path):
        self._set_icon_path = icon_path
        self.update()

    # MOVE TOOLTIP
    # ///////////////////////////////////////////////////////////////
    def move_tooltip(self):
        # GET MAIN WINDOW PARENT
        gp = self.mapToGlobal(QPoint(0, 0))

        # SET WIDGET TO GET POSTION
        # Return absolute position of widget inside app
        pos = self._parent.mapFromGlobal(gp)

        # FORMAT POSITION
        # Adjust tooltip position with offset
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self._top_margin

        # SET POSITION TO WIDGET
        # Move tooltip position
        self._tooltip.move(pos_x, pos_y)

# TOOLTIP
# ///////////////////////////////////////////////////////////////
class _ToolTip(QLabel):
    # TOOLTIP / LABEL StyleSheet
    style_tooltip = """ 
    QLabel {{		
        background-color: {_dark_one};	
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-right: 3px solid {_context_color};
        font: 800 9pt "Segoe UI";
    }}
    """
    def __init__(
        self,
        parent, 
        tooltip,
        dark_one,
        context_color,
        text_foreground
    ):
        QLabel.__init__(self)

        # LABEL SETUP
        style = self.style_tooltip.format(
            _dark_one = dark_one,
            _context_color = context_color,
            _text_foreground = text_foreground
        )
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)

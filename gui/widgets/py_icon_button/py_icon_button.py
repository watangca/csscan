# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# PY TITLE BUTTON
# ///////////////////////////////////////////////////////////////
class PyIconButton(QPushButton):
    def __init__(
        self,
        icon_path = None,
        parent = None,
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
        dark_one = "#1b1e23",
        text_foreground = "#8a95aa",
        context_color = "#568af2",
        top_margin = 40,
        is_active = False
    ):
        super().__init__(parent)
        self.update_rect()
        self.icons_cache = {}
        
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
        self._top_margin = top_margin
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
    def update_rect(self):
        self.rect = QRect(0, 0, self.width(), self.height())
        self.border_radius = self._set_border_radius

    def resizeEvent(self, event):
        self.update_rect()
        super().resizeEvent(event)

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._is_active:
            brush_color = self._context_color
        else:
            brush_color = self._set_bg_color

        brush = QBrush(QColor(brush_color))
        paint.setPen(Qt.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(self.rect, self.border_radius, self.border_radius)

        # DRAW ICONS
        self.icon_paint(paint, self._set_icon_path, self.rect)

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
    def icon_paint(self, qp, image, rect):
        # QPixmap 캐싱
        if image not in self.icons_cache:
            self.icons_cache[image] = QPixmap(image)

        icon = self.icons_cache[image]

        # 필요한 경우에만 QPainter 객체 생성
        if self._is_active or self._set_icon_color != QColor(0, 0, 0, 0):
            painter = QPainter(icon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            color = self._icon_color_active if self._is_active else self._set_icon_color
            painter.fillRect(icon.rect(), color)
            painter.end()

        # drawPixmap 위치 계산
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
        pos_x = (pos.x() - (self._tooltip.width() // 2)) + (self.width() // 2)
        pos_y = pos.y() - self._top_margin

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
        font: 800 9pt "Segoe UI";
    }}
    """
    def __init__(
        self,
        parent, 
        tooltip,
        dark_one,
        text_foreground
    ):
        QLabel.__init__(self)

        # LABEL SETUP
        style = self.style_tooltip.format(
            _dark_one = dark_one,
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

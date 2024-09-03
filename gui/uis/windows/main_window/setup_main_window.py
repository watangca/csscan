# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from .ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *

# FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from gui.core.functions import Functions

# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_dashboard",
            "btn_text" : "Dashboard",
            "btn_tooltip" : "Dashboard",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon" : "icon_svr.svg",
            "btn_id" : "btn_page_2",
            "btn_text" : "Asset Registration",
            "btn_tooltip" : "Asset Register",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_scan.svg",
            "btn_id" : "btn_page_3",
            "btn_text" : "Target Scan",
            "btn_tooltip" : "Target Scan",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_report.svg",
            "btn_id" : "btn_page_4",
            "btn_text" : "Reporting",
            "btn_tooltip" : "Reporting",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_info.svg",
            "btn_id" : "btn_info",
            "btn_text" : "Guideline",
            "btn_tooltip" : "Guideline",
            "show_top" : False,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_settings",
            "btn_text" : "Settings",
            "btn_tooltip" : "Settings",
            "show_top" : False,
            "is_active" : False
        }
    ]

     # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = [
        {
            "btn_icon" : "icon_search.svg",
            "btn_id" : "btn_search",
            "btn_tooltip" : "Search",
            "is_active" : False
        },
        {
            "btn_icon" : "icon_user.svg",
            "btn_id" : "btn_top_user",
            "btn_tooltip" : "Login User",
            "is_active" : False
        }
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("We give the right direction")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1_widget)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.menu_1,
            title = "Settings Left Column",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # Asset linux button
        self.btn_1 = PyPushButton(text= "Linux Asset")
        self.btn_1.setMinimumHeight(30)
        self.btn_1.setFixedWidth(170)
        self.ui.left_column.menus.btn_1_layout.addWidget(self.btn_1, Qt.AlignCenter, Qt.AlignCenter)

        # Asset  Windows button
        self.btn_2 = PyPushButton(text= "Windows Asset")
        self.btn_2.setMinimumHeight(30)
        self.btn_2.setFixedWidth(170)
        self.ui.left_column.menus.btn_2_layout.addWidget(self.btn_2, Qt.AlignCenter, Qt.AlignCenter)

        # Asset  Database button
        self.btn_3 = PyPushButton(text= "Database Asset")
        self.btn_3.setMinimumHeight(30)
        self.btn_3.setFixedWidth(170)
        self.ui.left_column.menus.btn_3_layout.addWidget(self.btn_3, Qt.AlignCenter, Qt.AlignCenter)

        # Linux scan button
        self.btn_4 = PyPushButton(text= "Linux Scan")
        self.btn_4.setMinimumHeight(30)
        self.btn_4.setFixedWidth(170)
        self.ui.left_column.menus.btn_4_layout.addWidget(self.btn_4, Qt.AlignCenter, Qt.AlignCenter)

        # Windows Scan Button
        self.btn_5 = PyPushButton(text= "Windows Scan")
        self.btn_5.setMinimumHeight(30)
        self.btn_5.setFixedWidth(170)
        self.ui.left_column.menus.btn_5_layout.addWidget(self.btn_5, Qt.AlignCenter, Qt.AlignCenter)

        # Database Scan Button
        self.btn_6 = PyPushButton(text= "Database Scan")
        self.btn_6.setMinimumHeight(30)
        self.btn_6.setFixedWidth(170)
        self.ui.left_column.menus.btn_6_layout.addWidget(self.btn_6, Qt.AlignCenter, Qt.AlignCenter)

        # Report Excel
        self.btn_7 = PyPushButton(text= "Excel Reporting")
        self.btn_7.setMinimumHeight(30)
        self.btn_7.setFixedWidth(170)
        self.ui.left_column.menus.btn_7_layout.addWidget(self.btn_7, Qt.AlignCenter, Qt.AlignCenter)

        # Report Word
        # self.btn_8 = PyPushButton(text= "Word Reporting")
        # self.btn_8.setMinimumHeight(30)
        # self.btn_8.setFixedWidth(170)
        # self.ui.left_column.menus.btn_8_layout.addWidget(self.btn_8, Qt.AlignCenter, Qt.AlignCenter)

        # Information - Linux Guide
        self.btn_9 = PyPushButton(text= "Linux Guide")
        self.btn_9.setMinimumHeight(30)
        self.btn_9.setFixedWidth(170)
        self.ui.left_column.menus.btn_9_layout.addWidget(self.btn_9, Qt.AlignCenter, Qt.AlignCenter)

        # Information - Linux Guide
        self.btn_10 = PyPushButton(text= "Windows Guide")
        self.btn_10.setMinimumHeight(30)
        self.btn_10.setFixedWidth(170)
        self.ui.left_column.menus.btn_10_layout.addWidget(self.btn_10, Qt.AlignCenter, Qt.AlignCenter)

        # Information - Linux Guide
        self.btn_11 = PyPushButton(text= "Database Guide")
        self.btn_11.setMinimumHeight(30)
        self.btn_11.setFixedWidth(170)
        self.ui.left_column.menus.btn_11_layout.addWidget(self.btn_11, Qt.AlignCenter, Qt.AlignCenter)

        # Settings - Account manager
        self.btn_12 = PyPushButton(text= "Account Management")
        self.btn_12.setMinimumHeight(30)
        self.btn_12.setFixedWidth(170)
        self.ui.left_column.menus.btn_12_layout.addWidget(self.btn_12, Qt.AlignCenter, Qt.AlignCenter)

        # Settings - Account history
        self.btn_13 = PyPushButton(text= "Account Hostory")
        self.btn_13.setMinimumHeight(30)
        self.btn_13.setFixedWidth(170)
        self.ui.left_column.menus.btn_13_layout.addWidget(self.btn_13, Qt.AlignCenter, Qt.AlignCenter)

        # Logout 버튼 추가
        self.btn_logout = PyPushButton(text="Logout")
        self.btn_logout.setMinimumHeight(30)
        self.btn_logout.setFixedWidth(170)
        self.ui.right_column.r_layout_1.addWidget(self.btn_logout, Qt.AlignCenter, Qt.AlignCenter)

        # Profile 버튼 추가
        self.btn_profile = PyPushButton(text="Profile")
        self.btn_profile.setMinimumHeight(30)
        self.btn_profile.setFixedWidth(170)
        self.ui.right_column.r_layout_2.addWidget(self.btn_profile, Qt.AlignCenter, Qt.AlignCenter)

        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import sys

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT LOGIN WINDOW
# ///////////////////////////////////////////////////////////////
from login.ui_login import *

# IMPORT Login SessionManager
# ///////////////////////////////////////////////////////////////
from login.sessionmanager import *
from login.usermanager import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# IMPORT Role [admin/user]
# ///////////////////////////////////////////////////////////////
from login.role_permissions import *
from login.database.UserDatabaseManager import get_user_db_connection

# IMPORT License Manager
# ///////////////////////////////////////////////////////////////
from login.license.licensemanager import determine_license_path, load_license_file, get_cpu_id


# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self, session_id=None, username=None):
        super().__init__()
        self.db_connection = get_user_db_connection()
        self.session_id = session_id
        self.username = username
        self.is_logout_confirmed = False

        # 세션 관리자 초기화
        self.session_manager = SessionManager(self.db_connection)

        # 라이센스 검증 수행
        self.verify_license('linux')
        self.verify_license('windows')
        self.verify_license('database')

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # Login user print
        formatted_tooltip = f"Logged in as: {username}"
        self.ui.title_bar.update_button_tooltip("btn_top_user", formatted_tooltip)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()


    def verify_license(self, license_type):
        try:
            license_path, key_path = determine_license_path("license", "license.key", "key.key")
            license_info = load_license_file(license_path, key_path)

            if not license_info:
                raise Exception("라이센스 정보가 유효하지 않습니다.")

            expiration_date = datetime.strptime(license_info.get("expiration_date"), '%Y-%m-%d')
            days_remaining = (expiration_date - datetime.now()).days

            if days_remaining < 0:
                raise Exception("라이센스가 만료되었습니다.")

            current_cpu_id = get_cpu_id()
            if license_info.get("cpu_id") != current_cpu_id:
                error_message = (f"CPU ID가 일치하지 않습니다.\n"
                                f"등록된 CPU ID: {license_info.get('cpu_id')}, 현재 CPU ID: {current_cpu_id}")
                raise Exception(error_message)

            max_usage_key = f"{license_type}_max_usage"  # 예: "linux_max_usage"
            max_usage = license_info.get(max_usage_key)
            if max_usage is None:
                raise Exception(f"{license_type} 라이센스 정보가 없습니다.")

            print(f"{license_type} 라이센스 검증 성공: 최대 사용 가능한 IP 개수 {max_usage} EA, 라이센스 만료까지 남은 일수: {days_remaining}일")

        except Exception as e:
            PyDialog.warning(self, "라이센스 오류", str(e) + "\n프로그램을 종료합니다.")
            sys.exit(-1)

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # Get Top Settings 
        top_btn_user = MainFunctions.get_title_bar_btn(self, "btn_top_user")

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # PAGE 1
        if btn.objectName() == "btn_dashboard":
            self.ui.left_menu.deselect_all()
            MainFunctions.toggle_left_column(self)
            self.ui.left_menu.deselect_all_tab()
            self.ui.left_menu.select_only_one(btn.objectName())
            MainFunctions.set_page(self, self.ui.load_pages.page_1_widget)
        else:
            dashboard_button = self.ui.left_menu.findChild(QPushButton, "btn_dashboard")
            if dashboard_button and dashboard_button.is_active():
                dashboard_button.set_active(False)

        # PAGE 2
        if btn.objectName() == "btn_page_2" or btn.objectName() == "btn_close_left_column":
            top_btn_user.set_active(False)
            if not MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu= self.ui.left_column.menus.menu_1,
                    title= "Asset registration",
                    icon_path= Functions.set_svg_icon("icon_svr.svg")
                )
                # Asset Registration Sub Button Clicked 
                self.btn_1.clicked.connect(self.on_linux_asset_clicked)
                self.btn_2.clicked.connect(self.on_windows_asset_clicked)
                self.btn_3.clicked.connect(self.on_database_asset_clicked)

        # PAGE 3
        if btn.objectName() == "btn_page_3" or btn.objectName() == "btn_close_left_column":
            top_btn_user.set_active(False)
            if not MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            if btn.objectName() !="btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu= self.ui.left_column.menus.menu_2,
                    title= "Target Scan",
                    icon_path= Functions.set_svg_icon("icon_scan.svg")
                )
                # Target Scan Sub Button Clicked 
                self.btn_4.clicked.connect(self.on_linux_scan_clicked)
                self.btn_5.clicked.connect(self.on_windows_scan_clicked)
                self.btn_6.clicked.connect(self.on_database_scan_clicked)

        # PAGE 4
        if btn.objectName() == "btn_page_4" or btn.objectName() == "btn_close_left_column":
            top_btn_user.set_active(False)
            if not MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            if btn.objectName() !="btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu= self.ui.left_column.menus.menu_3,
                    title= "Reporting",
                    icon_path= Functions.set_svg_icon("icon_report.svg")
                )
                # Reporting Sub Button Clicked 
                self.btn_7.clicked.connect(self.on_excel_report_clicked)
                # self.btn_8.clicked.connect(self.on_word_report_clicked)

        # Guideline
        if btn.objectName() == "btn_info" or btn.objectName() == "btn_close_left_column":
            top_btn_user.set_active(False)
            if not MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            if btn.objectName() !="btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu= self.ui.left_column.menus.menu_4,
                    title= "Guideline",
                    icon_path= Functions.set_svg_icon("icon_info.svg")
                )
                self.btn_9.clicked.connect(self.on_linux_guide_clicked)
                self.btn_10.clicked.connect(self.on_windows_guide_clicked)
                self.btn_11.clicked.connect(self.on_database_guide_clicked)
        
        # Settings tab
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            top_btn_user.set_active(False)
            if not MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            if btn.objectName() !="btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu= self.ui.left_column.menus.menu_5,
                    title= "Settings tab",
                    icon_path= Functions.set_svg_icon("icon_settings.svg")
                )
                self.btn_12.clicked.connect(self.on_account_management_clicked)
                self.btn_13.clicked.connect(self.on_account_history_clicked)

        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_user":
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)
                MainFunctions.toggle_right_column(self)

            btn_settings = MainFunctions.get_left_menu_btn(self, "btn_page_2")
            btn_settings.set_active_tab(False)     
          
            btn_info = MainFunctions.get_left_menu_btn(self, "btn_page_3")
            btn_info.set_active_tab(False)     
         
            btn_settings = MainFunctions.get_left_menu_btn(self, "btn_page_4")
            btn_settings.set_active_tab(False)     
         
            btn_info = MainFunctions.get_left_menu_btn(self, "btn_info")
            btn_info.set_active_tab(False)     
      
            btn_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            btn_settings.set_active_tab(False)  

            self.btn_logout.clicked.connect(self.on_logout_clicked)
            self.btn_profile.clicked.connect(self.on_profile_clicked) 
        

        # BTN Search
        if btn.objectName() == "btn_search":
            # 오른쪽 컬럼이 보이는 상태라면 숨김 처리
            if MainFunctions.right_column_is_visible(self):
                top_btn_user = MainFunctions.get_title_bar_btn(self, "btn_top_user")
                top_btn_user.set_active(False)
                MainFunctions.toggle_right_column(self)

            # page_8 위젯으로 전환
            MainFunctions.set_page(self, self.ui.load_pages.page_8_widget)
              

    def on_linux_asset_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_2_linux_widget)        
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    def on_windows_asset_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_2_windows_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    def on_database_asset_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_2_database_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    def on_linux_scan_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_3_linux_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    def on_windows_scan_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_3_windows_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    def on_database_scan_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_3_database_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)
    
    def on_excel_report_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_4_excel_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    # def on_word_report_clicked(self):
    #     MainFunctions.set_page(self, self.ui.load_pages.page_4_word_widget)
    #     role_handler = RoleBasedHandler(self, self.username)
    #     user_role = role_handler.get_user_role()
    #     role_handler.disable_buttons_for_user_role(self, user_role)
    
    def on_linux_guide_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_5_linux_widget)

    def on_windows_guide_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_5_windows_widget)

    def on_database_guide_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_5_database_widget)

    def on_account_management_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_6_management_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    def on_account_history_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_6_history_widget)
        role_handler = RoleBasedHandler(self, self.username)
        user_role = role_handler.get_user_role()
        role_handler.disable_buttons_for_user_role(self, user_role)

    def on_logout_clicked(self):
        if not hasattr(self, 'logout_confirmation_msg') or not self.logout_confirmation_msg.isVisible():
            self.logout_confirmation_msg = PyChoiceBox('로그아웃 확인', '로그아웃 하시겠습니까?')
            reply = self.logout_confirmation_msg.exec()

            if reply == QDialog.Accepted:
                db_connection = get_user_db_connection()
                session_manager = SessionManager(db_connection)
                session_manager.logout(self.session_id)
                self.is_logout_confirmed = True  
                self.close()
        
    def on_profile_clicked(self):
        MainFunctions.set_page(self, self.ui.load_pages.page_7_widget)

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        # print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = QCursor.pos()

    def closeEvent(self, event):
        # 로그아웃 확인이 이전에 완료되지 않았을 경우에만 로그아웃 확인 대화 상자 표시
        if not self.is_logout_confirmed:
            logout_confirmation_msg = PyChoiceBox('로그아웃 확인', '로그아웃 하시겠습니까?')
            reply = logout_confirmation_msg.exec()

            if reply == QDialog.Accepted:
                session_manager = SessionManager(self.db_connection)
                session_manager.logout(self.session_id)
                event.accept()
            else:
                event.ignore()
        else:
            # 이미 로그아웃이 확인된 경우
            event.accept()

# LOGIN WINDOW CLASS
# ///////////////////////////////////////////////////////////////
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SET UP THE LOGIN UI
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

    def check_credentials_and_login(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # 애플리케이션 생성
    app = QApplication(sys.argv)

    # 현재 화면의 DPI 감지
    screen = QGuiApplication.primaryScreen()
    screen_dpi = screen.logicalDotsPerInch()
    scale_factor = screen_dpi / 144.0  # 기본 DPI인 96을 기준으로 스케일 팩터 계산

    # 환경 변수 설정
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_SCALE_FACTOR"] = str(scale_factor)  # 동적으로 계산된 스케일 팩터 사용
    os.environ["QT_FONT_DPI"] = str(int(screen_dpi))  # 화면 DPI를 그대로 사용

    # High DPI 스케일링 설정 (새로운 방식)
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    # 시스템 폰트 설정 (안티앨리어싱 포함)
    font = QFont()
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    app.setWindowIcon(QIcon("icon.ico"))

    # 로그인 창 클래스 정의
    class LoginWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            # 로그인 UI 설정
            self.ui = Ui_LoginWindow()
            self.ui.setupUi(self)

        def check_credentials_and_login(self):
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()

    # 로그인 창 표시
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())
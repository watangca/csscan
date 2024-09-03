from qt_core import *
from gui.widgets import *
from login.database.UserDatabaseManager import get_user_db_connection

class RoleBasedHandler:
    def __init__(self, window, username):
        self.window = window
        self.username = username

    def get_user_role(self):
        with get_user_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = ?", (self.username,))
            result = cursor.fetchone()
            return result[0] if result else None

    def is_user_role(self):
        user_role = self.get_user_role()
        return user_role == 'user'
    
    def disable_buttons_for_user_role(self, window, user_role):
        if user_role == 'user':

            # Page_2_linux 페이지의 버튼 비활성화
            window.ui.load_pages.page_2_linux_widget.registerButton.setDisabled(True)
            window.ui.load_pages.page_2_linux_widget.deleteButton.setDisabled(True)
            window.ui.load_pages.page_2_linux_widget.uploadButton.setDisabled(True)

            # Page_2_widnows 페이지의 버튼 비활성화
            window.ui.load_pages.page_2_windows_widget.registerButton.setDisabled(True)
            window.ui.load_pages.page_2_windows_widget.deleteButton.setDisabled(True)
            window.ui.load_pages.page_2_windows_widget.uploadButton.setDisabled(True)

            # Page_2_database 페이지의 버튼 비활성화
            window.ui.load_pages.page_2_database_widget.registerButton.setDisabled(True)
            window.ui.load_pages.page_2_database_widget.deleteButton.setDisabled(True)
            window.ui.load_pages.page_2_database_widget.uploadButton.setDisabled(True)

            # Page_3_linux 페이지의 버튼 비활성화
            page_3_linux_widget = window.ui.load_pages.page_3_linux_widget
            # 점검 수행 탭의 버튼 비활성화
            for i in range(page_3_linux_widget.check_table.rowCount()):
                cell_widget = page_3_linux_widget.check_table.cellWidget(i, 4)
                button = cell_widget.findChild(QPushButton)
                button.setDisabled(True)
            # 점검 결과 탭의 버튼 비활성화
            for i in range(page_3_linux_widget.result_table.rowCount()):
                detail_view_widget = page_3_linux_widget.result_table.cellWidget(i, 4)
                detail_view_button = detail_view_widget.findChild(QPushButton)
                detail_view_button.setDisabled(False)
                export_widget = page_3_linux_widget.result_table.cellWidget(i, 5)
                export_button = export_widget.findChild(QPushButton)
                export_button.setDisabled(False)

            # Page_3_widnows 페이지의 버튼 비활성화
            page_3_windows_widget = window.ui.load_pages.page_3_windows_widget
            # 점검 수행 탭의 버튼 비활성화
            for i in range(page_3_windows_widget.check_table.rowCount()):
                cell_widget = page_3_windows_widget.check_table.cellWidget(i, 4)
                button = cell_widget.findChild(QPushButton)
                button.setDisabled(True)
            # 점검 결과 탭의 버튼 비활성화
            for i in range(page_3_windows_widget.result_table.rowCount()):
                detail_view_widget = page_3_windows_widget.result_table.cellWidget(i, 4)
                detail_view_button = detail_view_widget.findChild(QPushButton)
                detail_view_button.setDisabled(False)
                export_widget = page_3_windows_widget.result_table.cellWidget(i, 5)
                export_button = export_widget.findChild(QPushButton)
                export_button.setDisabled(False)

            # Page_3_database 페이지의 버튼 비활성화
            page_3_database_widget = window.ui.load_pages.page_3_database_widget
            # 점검 수행 탭의 버튼 비활성화
            for i in range(page_3_database_widget.check_table.rowCount()):
                cell_widget = page_3_database_widget.check_table.cellWidget(i, 4)
                button = cell_widget.findChild(QPushButton)
                button.setDisabled(True)
            # 점검 결과 탭의 버튼 비활성화
            for i in range(page_3_database_widget.result_table.rowCount()):
                detail_view_widget = page_3_database_widget.result_table.cellWidget(i, 4)
                detail_view_button = detail_view_widget.findChild(QPushButton)
                detail_view_button.setDisabled(False)
                export_widget = page_3_database_widget.result_table.cellWidget(i, 5)
                export_button = export_widget.findChild(QPushButton)
                export_button.setDisabled(False)

            # Page_4_excel 페이지의 버튼 비활성화
            page_4_excel_widget = window.ui.load_pages.page_4_excel_widget
            page_4_excel_widget.btn_new_report.setDisabled(True)
            page_4_excel_widget.btn_delete_history.setDisabled(True)
            
            # Page_4_excel 페이지 테이블의 'Export' 버튼 비활성화
            for i in range(page_4_excel_widget.report_table.rowCount()):
                cell_widget = page_4_excel_widget.report_table.cellWidget(i, 4)
                button = cell_widget.findChild(PyTableButton)
                button.setDisabled(True)

            # Page_6_management 페이지의 버튼 비활성화
            page_6_management_widget = window.ui.load_pages.page_6_management_widget
            page_6_management_widget.add_account_btn.setDisabled(True)   
            page_6_management_widget.edit_account_btn.setDisabled(True) 
            page_6_management_widget.delete_account_btn.setDisabled(True) 

            # Page_6_history 페이지의 검색 버튼 비활성화
            page_6_history_widget = window.ui.load_pages.page_6_history_widget
            page_6_history_widget.search_button.setDisabled(True) 

            self.show_warning_message(window)

    def show_warning_message(self, window):
        PyDialog.warning(window, "경고", "로그인한 계정은 이 페이지에 대한 작업 권한이 없습니다.")

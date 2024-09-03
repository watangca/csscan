from qt_core import *
from login.auth_module import *
from login.sessionmanager import *
from gui.widgets import *
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from login.database.UserDatabaseManager import get_user_db_connection

class Page6ManagementWidget(QWidget):
    def __init__(self):
        super().__init__()

        # LOAD SETTINGS
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        themes = Themes()
        self.themes = themes.items

        self.db_connection = get_user_db_connection()
        self.setup_ui()
        self.load_accounts()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.management_layout = QHBoxLayout()

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.management_layout.addItem(spacer)

        self.add_account_btn = PyPushButton("계정 등록")
        self.edit_account_btn = PyPushButton("계정 편집")
        self.delete_account_btn = PyPushButton("계정 삭제")
        
        self.management_layout.addWidget(self.add_account_btn)
        self.management_layout.addWidget(self.edit_account_btn)
        self.management_layout.addWidget(self.delete_account_btn)

        # 버튼 클릭 이벤트 연결
        self.add_account_btn.clicked.connect(self.add_account)
        self.edit_account_btn.clicked.connect(self.edit_account)
        self.delete_account_btn.clicked.connect(self.delete_account)


        self.layout.addLayout(self.management_layout)

        self.account_table = PyTableWidget()
        self.setup_account_table()
        self.layout.addWidget(self.account_table)

    def setup_account_table(self):
        self.account_table.setColumnCount(6)
        self.account_table.setHorizontalHeaderLabels(["No", "사용자 계정명", "패스워드", "접속 권한", "이메일", "계정 잠김 상태"])        
        header = self.account_table.horizontalHeader()
        for i in range(self.account_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)        
        self.load_accounts()

    def load_accounts(self):
        self.account_table.setRowCount(0)

        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role, email, account_locked FROM users")
            for row_number, row_data in enumerate(cursor.fetchall()):
                self.account_table.insertRow(row_number)
                no_item = QTableWidgetItem(str(row_number + 1))
                no_item.setTextAlignment(Qt.AlignCenter)  # No 열을 중앙 정렬합니다.
                self.account_table.setItem(row_number, 0, no_item)

                for column_number, data in enumerate(row_data[1:]):  # id 값을 제외하고 데이터 할당
                    if column_number == 1:  # 패스워드 열의 경우 마스킹 처리
                        item = QTableWidgetItem("******")
                    elif column_number == 4:  # 계정 잠김 상태 열
                        item = QTableWidgetItem("잠김" if data == 1 else "활성")
                    else:
                        item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.account_table.setItem(row_number, column_number + 1, item)

    def add_account(self):
        dialog = PyAccountDialog(mode="add")
        if dialog.exec():
            account_info = {
                "username": dialog.username_entry.text(),
                "email": dialog.email_entry.text(),
                "password": dialog.password_entry.text(),
                "role": dialog.role_entry.text()
            }
            try:
                with self.db_connection as conn:
                    cursor = conn.cursor()
                    hashed_password = hash_password(account_info['password'])
                    cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                                   (account_info['username'], account_info['email'], hashed_password, account_info['role']))
                    conn.commit()
                PyDialog.information(self, "성공", "계정이 성공적으로 추가되었습니다.")
                self.load_accounts()
            except Exception as e:
                PyDialog.warning(self, "실패", "계정 추가 중 오류가 발생했습니다: " + str(e))

    def edit_account(self):
        selected_items = self.account_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            account_data = {
                "username": self.account_table.item(row, 1).text(),
                "email": self.account_table.item(row, 4).text(),
                "role": self.account_table.item(row, 3).text()
            }
            dialog = PyAccountDialog(mode="edit", account_data=account_data)
            if dialog.exec():
                updated_account_info = {
                    "username": dialog.username_entry.text(),
                    "email": dialog.email_entry.text(),
                    "role": dialog.role_entry.text(),
                    "password": dialog.password_entry.text()  # 비밀번호 필드 추가
                }
                try:
                    with self.db_connection as conn:
                        cursor = conn.cursor()
                        hashed_password = hash_password(updated_account_info['password'])  # 비밀번호 해시 처리
                        # Update the user's email, role and password
                        cursor.execute("UPDATE users SET email=?, role=?, password=? WHERE username=?",
                                    (updated_account_info['email'], updated_account_info['role'], hashed_password, updated_account_info['username']))
                        conn.commit()
                    PyDialog.information(self, "성공", "계정이 성공적으로 편집되었습니다.")
                    self.load_accounts()
                except Exception as e:
                    PyDialog.warning(self, "실패", "계정 편집 중 오류가 발생했습니다: " + str(e))

    def delete_account(self):
        selected_items = self.account_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            account_data = {
                "username": self.account_table.item(row, 1).text(),
                "email": self.account_table.item(row, 4).text(),
                "role": self.account_table.item(row, 3).text()
            }
            dialog = PyAccountDialog(mode="delete", account_data=account_data)
            if dialog.exec():
                entered_password = dialog.password_entry.text()
                
                # 비밀번호 검증 로직
                conn = get_user_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT password FROM users WHERE username = ?', (account_data["username"],))
                result = cursor.fetchone()
                if result:
                    stored_password = result[0]
                    if verify_password(stored_password, entered_password):
                        # 비밀번호가 일치하면 계정 삭제
                        try:
                            cursor.execute("DELETE FROM users WHERE username=?", (account_data["username"],))
                            conn.commit()
                            PyDialog.information(self, "성공", "계정이 성공적으로 삭제되었습니다.")
                            self.load_accounts()
                        except Exception as e:
                            PyDialog.warning(self, "실패", "계정 삭제 중 오류가 발생했습니다: " + str(e))
                    else:
                        # 비밀번호 불일치
                        PyDialog.warning(self, "실패", "비밀번호가 올바르지 않습니다.")
                else:
                    # 계정이 존재하지 않음
                    PyDialog.warning(self, "실패", "계정이 존재하지 않습니다.")
                
                conn.close()



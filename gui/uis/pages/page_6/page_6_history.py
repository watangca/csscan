from qt_core import *
from login.auth_module import *
from login.sessionmanager import *
from gui.widgets import *
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from login.database.UserDatabaseManager import get_user_db_connection

class Page6HistoryWidget(QWidget):
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
        self.load_history()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        # Set up search and delete layout
        self.actions_layout = QHBoxLayout()

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.actions_layout.addItem(spacer)

        self.search_bar = PyLineEdit(place_holder_text="Search account history")
        self.actions_layout.addWidget(self.search_bar)
        self.search_button = PyPushButton("검색")
        self.actions_layout.addWidget(self.search_button)
        
        # Add a delete button
        self.delete_button = PyPushButton("삭제")
        self.actions_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.actions_layout)

        self.history_table = PyTableWidget()
        self.setup_history_table()
        self.layout.addWidget(self.history_table)

        self.search_button.clicked.connect(self.search_history)
        self.delete_button.clicked.connect(self.delete_selected_history)

    def setup_history_table(self):
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["접속 계정", "로그인 시간", "로그아웃 시간", "로그인 성공여부", "접속 IP"])
        header = self.history_table.horizontalHeader()
        for i in range(self.history_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_history(self, search_query=None):
        search_query = f"%{search_query}%" if search_query else "%"
        with self.db_connection as conn:
            cursor = conn.cursor()
            query = """
            SELECT u.username, s.login_time, s.logout_time, la.success, la.ip_address
            FROM sessions s
            INNER JOIN login_attempts la ON s.session_id = la.session_id
            INNER JOIN users u ON u.username = s.username
            WHERE (u.username LIKE ? OR la.ip_address LIKE ?)
            ORDER BY s.login_time DESC
            """
            cursor.execute(query, (search_query, search_query))
            rows = cursor.fetchall()

            self.history_table.setRowCount(0)

            for row_number, row_data in enumerate(rows):
                self.history_table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem("성공" if data == 1 and column_number == 3 else str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.history_table.setItem(row_number, column_number, item)

    def delete_selected_history(self):
        selected_rows = self.history_table.selectionModel().selectedRows()
        rows_to_delete = [r.row() for r in selected_rows]

        if not rows_to_delete:
            PyDialog.warning(self, "경고", "삭제할 이력을 선택하세요.")
            return

        
        choice_box = PyChoiceBox("삭제 확인", "선택한 이력을 정말 삭제하시겠습니까?")
        reply = choice_box.exec()

        if reply == QDialog.Accepted:
            with self.db_connection as conn:
                cursor = conn.cursor()
                for row in rows_to_delete:
                    username = self.history_table.item(row, 0).text()
                    login_time = self.history_table.item(row, 1).text()
                    # Adjust the deletion query based on your schema
                    query = "DELETE FROM sessions WHERE username=? AND login_time=?"
                    cursor.execute(query, (username, login_time))
                conn.commit()

            self.load_history()

    def search_history(self):
        search_query = self.search_bar.text()
        self.load_history(search_query)
